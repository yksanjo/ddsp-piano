const fs = require('fs');
const path = require('path');
const csvParser = require('./parsers/csvParser');
const swiftParser = require('./parsers/swiftParser');
const tradeComparator = require('./comparators/tradeComparator');
const calypsoClient = require('./services/calypsoClient');
const reportGenerator = require('./utils/reportGenerator');
const emailService = require('./utils/emailService');
const logger = require('./utils/logger');

class ReconciliationEngine {
  constructor() {
    this.discrepancies = [];
  }

  async reconcile(calypsoTrades, externalFile, fileType = 'csv') {
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
      this.discrepancies = tradeComparator.compare(calypsoTrades, externalTrades);

      logger.info(`Found ${this.discrepancies.length} discrepancies`);

      return {
        calypsoCount: calypsoTrades.length,
        externalCount: externalTrades.length,
        matched: calypsoTrades.length - this.discrepancies.length,
        discrepancies: this.discrepancies
      };
    } catch (error) {
      logger.error('Reconciliation error', error);
      throw error;
    }
  }

  async reconcileFromCalypso(externalFile, fileType = 'csv') {
    logger.info('Fetching trades from Calypso API');
    const calypsoTrades = await calypsoClient.getTrades();
    return this.reconcile(calypsoTrades, externalFile, fileType);
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



