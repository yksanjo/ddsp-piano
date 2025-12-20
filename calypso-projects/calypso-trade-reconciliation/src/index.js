#!/usr/bin/env node

const reconciliationEngine = require('./reconciliationEngine');
const config = require('./config/config');
const logger = require('./utils/logger');
const path = require('path');

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length < 1) {
    console.log('Usage: node src/index.js <external-file> [file-type]');
    console.log('  external-file: Path to CSV or SWIFT file');
    console.log('  file-type: csv or swift (default: csv)');
    process.exit(1);
  }

  const externalFile = args[0];
  const fileType = args[1] || 'csv';

  try {
    logger.info('Starting trade reconciliation...');

    // Reconcile trades
    const result = await reconciliationEngine.reconcileFromCalypso(externalFile, fileType);

    console.log('\nReconciliation Results:');
    console.log(`  Calypso Trades: ${result.calypsoCount}`);
    console.log(`  External Trades: ${result.externalCount}`);
    console.log(`  Matched: ${result.matched}`);
    console.log(`  Discrepancies: ${result.discrepancies.length}`);

    // Generate report
    const reportPath = path.join(process.cwd(), `reconciliation-report-${Date.now()}.txt`);
    await reconciliationEngine.generateReport(reportPath);
    console.log(`\nReport saved to: ${reportPath}`);

    // Send email if enabled and discrepancies found
    if (result.discrepancies.length > 0 && config.email.enabled) {
      await reconciliationEngine.sendEmailNotification(config);
      console.log('Email notification sent');
    }

    process.exit(result.discrepancies.length > 0 ? 1 : 0);
  } catch (error) {
    logger.error('Reconciliation failed', error);
    console.error('Error:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { main };



