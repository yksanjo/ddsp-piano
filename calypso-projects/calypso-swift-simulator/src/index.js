#!/usr/bin/env node

const swiftGenerator = require('./swiftGenerator');
const calypsoClient = require('./services/calypsoClient');
const fs = require('fs');
const path = require('path');
const logger = require('./utils/logger');

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length < 1) {
    console.log('Usage: node src/index.js <message-type> [trade-id] [output-file]');
    console.log('  message-type: MT103 or MT300');
    console.log('  trade-id: Optional trade ID (if not provided, uses mock data)');
    console.log('  output-file: Optional output file path');
    process.exit(1);
  }

  const messageType = args[0].toUpperCase();
  const tradeId = args[1];
  const outputFile = args[2];

  try {
    let tradeData;

    if (tradeId) {
      // Fetch trade from Calypso
      tradeData = await calypsoClient.getTradeById(tradeId);
      if (!tradeData) {
        console.error(`Trade not found: ${tradeId}`);
        process.exit(1);
      }
    } else {
      // Use mock data
      logger.info('No trade ID provided, using mock data');
      tradeData = {
        id: 'TRD-001',
        tradeDate: new Date(),
        counterparty: 'Deutsche Bank',
        instrument: 'USD/EUR',
        notional: 1000000,
        currency: 'USD',
        rate: 1.10
      };
    }

    // Generate SWIFT message
    const result = swiftGenerator.generate(tradeData, messageType);

    if (outputFile) {
      fs.writeFileSync(outputFile, result.message, 'utf8');
      console.log(`SWIFT message saved to: ${outputFile}`);
    } else {
      console.log('\nGenerated SWIFT Message:');
      console.log('='.repeat(50));
      console.log(result.message);
      console.log('='.repeat(50));
    }

    if (!result.valid) {
      console.warn('\nValidation warnings:');
      result.errors.forEach(error => console.warn(`  - ${error}`));
    }

    process.exit(0);
  } catch (error) {
    logger.error('SWIFT generation failed', error);
    console.error('Error:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { main };



