const logger = require('./logger');

class ReportGenerator {
  generate(discrepancies) {
    const timestamp = new Date().toISOString();
    let report = `\n`;
    report += `========================================\n`;
    report += `TRADE RECONCILIATION REPORT\n`;
    report += `Generated: ${timestamp}\n`;
    report += `========================================\n\n`;

    report += `SUMMARY\n`;
    report += `-------\n`;
    report += `Total Discrepancies: ${discrepancies.length}\n\n`;

    const byType = discrepancies.reduce((acc, disc) => {
      acc[disc.type] = (acc[disc.type] || 0) + 1;
      return acc;
    }, {});

    Object.keys(byType).forEach(type => {
      report += `${type}: ${byType[type]}\n`;
    });

    report += `\n\nDETAILS\n`;
    report += `-------\n\n`;

    discrepancies.forEach((disc, index) => {
      report += `${index + 1}. Trade ID: ${disc.tradeId}\n`;
      report += `   Type: ${disc.type}\n`;

      if (disc.type === 'field_mismatch') {
        disc.fields.forEach(field => {
          report += `   Field: ${field.field}\n`;
          report += `     Adenza: ${field.Adenza}\n`;
          report += `     External: ${field.external}\n`;
        });
      } else if (disc.type === 'missing_in_external') {
        report += `   Trade exists in Adenza but not in external file\n`;
        report += `   Adenza Data: ${JSON.stringify(disc.Adenza, null, 2)}\n`;
      } else if (disc.type === 'missing_in_Adenza') {
        report += `   Trade exists in external file but not in Adenza\n`;
        report += `   External Data: ${JSON.stringify(disc.external, null, 2)}\n`;
      }

      report += `\n`;
    });

    return report;
  }
}

module.exports = new ReportGenerator();

