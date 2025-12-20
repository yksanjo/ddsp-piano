const fs = require('fs');
const path = require('path');
const csvParser = require('./parsers/csvParser');
const swiftParser = require('./parsers/swiftParser');
const tradeComparator = require('./comparators/tradeComparator');
const AdenzaClient = require('./services/AdenzaClient');
const reportGenerator = require('./utils/reportGenerator');
const emailService = require('./utils/emailService');
const logger = require('./utils/logger');

class ReconciliationEngine {
  constructor() {
    this.discrepancies = [];
  }

  async reconcile(AdenzaTrades, externalFile, fileType = 'csv') {
    logger.info(`Starting reconciliation: ${externalFile} (${fileType})`);

    let externalTrades = [];
    
    try {
      if (fileType === 'csv') {
        externalTrades = await csvParser.parse(externalFile);
      } else if (fileType === 'swift') {
        externalTrades = await swiftParser.parse(externalFile);
      } else {
        throw new Error(`Unsupported file type: ${fileType}`);
      }

      logger.info(`Parsed ${externalTrades.length} external trades`);

      // Match trades and find discrepancies
      this.discrepancies = tradeComparator.compare(AdenzaTrades, externalTrades);

      logger.info(`Found ${this.discrepancies.length} discrepancies`);

      return {
        AdenzaCount: AdenzaTrades.length,
        externalCount: externalTrades.length,
        matched: AdenzaTrades.length - this.discrepancies.length,
        discrepancies: this.discrepancies
      };
    } catch (error) {
      logger.error('Reconciliation error', error);
      throw error;
    }
  }

  async reconcileFromAdenza(externalFile, fileType = 'csv') {
    logger.info('Fetching trades from Adenza API');
    const AdenzaTrades = await AdenzaClient.getTrades();
    return this.reconcile(AdenzaTrades, externalFile, fileType);
  }

  async generateReport(outputPath) {
    logger.info(`Generating reconciliation report: ${outputPath}`);
    const report = reportGenerator.generate(this.discrepancies);
    
    fs.writeFileSync(outputPath, report, 'utf8');
    logger.info(`Report saved to ${outputPath}`);
    
    return outputPath;
  }

  async sendEmailNotification(config) {
    if (!config.email.enabled) {
      logger.info('Email notifications disabled');
      return;
    }

    try {
      const report = reportGenerator.generate(this.discrepancies);
      await emailService.send({
        to: config.email.to,
        from: config.email.from,
        subject: 'Trade Reconciliation Report - Discrepancies Found',
        text: `Found ${this.discrepancies.length} discrepancies. See attached report.`,
        html: `<p>Found <strong>${this.discrepancies.length}</strong> discrepancies.</p><pre>${report}</pre>`,
        attachments: [{
          filename: 'reconciliation-report.txt',
          content: report
        }]
      }, config.email.smtp);
      
      logger.info('Email notification sent');
    } catch (error) {
      logger.error('Failed to send email notification', error);
    }
  }
}

module.exports = new ReconciliationEngine();

