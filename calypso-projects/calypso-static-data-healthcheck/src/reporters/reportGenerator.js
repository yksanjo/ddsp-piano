const fs = require('fs');
const logger = require('../utils/logger');

class ReportGenerator {
  generate(issues, stats) {
    const timestamp = new Date().toISOString();
    let report = `\n`;
    report += `========================================\n`;
    report += `CALYPSO STATIC DATA HEALTH CHECK REPORT\n`;
    report += `Generated: ${timestamp}\n`;
    report += `========================================\n\n`;

    // Summary
    report += `SUMMARY\n`;
    report += `-------\n`;
    report += `Health Score: ${this.calculateScore(issues, stats)}%\n\n`;

    report += `Legal Entities:\n`;
    report += `  Total: ${stats.legalEntities.total}\n`;
    report += `  Valid: ${stats.legalEntities.valid}\n`;
    report += `  Invalid: ${stats.legalEntities.invalid}\n\n`;

    report += `Books:\n`;
    report += `  Total: ${stats.books.total}\n`;
    report += `  Valid: ${stats.books.valid}\n`;
    report += `  Invalid: ${stats.books.invalid}\n\n`;

    report += `Portfolios:\n`;
    report += `  Total: ${stats.portfolios.total}\n`;
    report += `  Valid: ${stats.portfolios.valid}\n`;
    report += `  Invalid: ${stats.portfolios.invalid}\n\n`;

    // Issues
    if (issues.length > 0) {
      report += `ISSUES\n`;
      report += `------\n\n`;

      issues.forEach((issue, index) => {
        report += `${index + 1}. ${issue.type.toUpperCase()}: ${issue.entity || issue.book || issue.portfolio}\n`;
        issue.issues.forEach(error => {
          report += `   - ${error}\n`;
        });
        report += `\n`;
      });
    } else {
      report += `No issues found. All static data is valid.\n`;
    }

    return report;
  }

  calculateScore(issues, stats) {
    const total = stats.legalEntities.total + 
                  stats.books.total + 
                  stats.portfolios.total;
    const invalid = stats.legalEntities.invalid + 
                    stats.books.invalid + 
                    stats.portfolios.invalid;

    if (total === 0) return 100;
    return Math.round(((total - invalid) / total) * 100);
  }

  async saveReport(report, filePath) {
    try {
      fs.writeFileSync(filePath, report, 'utf8');
      logger.info(`Report saved to ${filePath}`);
      return filePath;
    } catch (error) {
      logger.error('Failed to save report', error);
      throw error;
    }
  }
}

module.exports = new ReportGenerator();



