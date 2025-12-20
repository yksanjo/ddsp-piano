#!/usr/bin/env node

const healthCheck = require('./healthcheck');
const reportGenerator = require('./reporters/reportGenerator');
const logger = require('./utils/logger');
const path = require('path');
const fs = require('fs');

async function main() {
  try {
    logger.info('Starting static data health check...');

    const result = await healthCheck.run();

    console.log('\nHealth Check Results:');
    console.log(`  Health Score: ${result.score}%`);
    console.log(`  Total Issues: ${result.issues.length}`);
    console.log(`  Legal Entities: ${result.stats.legalEntities.valid}/${result.stats.legalEntities.total} valid`);
    console.log(`  Books: ${result.stats.books.valid}/${result.stats.books.total} valid`);
    console.log(`  Portfolios: ${result.stats.portfolios.valid}/${result.stats.portfolios.total} valid`);

    // Save report
    const reportPath = path.join(process.cwd(), `health-check-report-${Date.now()}.txt`);
    await reportGenerator.saveReport(result.report, reportPath);
    console.log(`\nReport saved to: ${reportPath}`);

    // Exit with appropriate code
    process.exit(result.issues.length > 0 ? 1 : 0);
  } catch (error) {
    logger.error('Health check failed', error);
    console.error('Error:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { main };



