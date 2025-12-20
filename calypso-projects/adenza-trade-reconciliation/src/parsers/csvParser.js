const fs = require('fs');
const Papa = require('papaparse');
const logger = require('../utils/logger');

class CSVParser {
  async parse(filePath) {
    try {
      const fileContent = fs.readFileSync(filePath, 'utf8');
      
      return new Promise((resolve, reject) => {
        Papa.parse(fileContent, {
          header: true,
          skipEmptyLines: true,
          transformHeader: (header) => {
            // Normalize header names
            return header.trim().toLowerCase()
              .replace(/\s+/g, '_')
              .replace(/trade_id|tradeid|id/, 'trade_id')
              .replace(/trade_date|tradedate|date/, 'trade_date')
              .replace(/notional|amount|value/, 'notional')
              .replace(/counterparty|cpty/, 'counterparty')
              .replace(/instrument|inst/, 'instrument');
          },
          complete: (results) => {
            if (results.errors.length > 0) {
              logger.warn('CSV parsing warnings', results.errors);
            }
            
            const trades = results.data.map((row, index) => ({
              trade_id: row.trade_id || `EXTERNAL-${index + 1}`,
              trade_date: row.trade_date,
              counterparty: row.counterparty,
              instrument: row.instrument,
              notional: parseFloat(row.notional) || 0,
              currency: row.currency || 'USD',
              status: row.status || 'Unknown',
              source: 'external_csv'
            }));

            logger.info(`Parsed ${trades.length} trades from CSV`);
            resolve(trades);
          },
          error: (error) => {
            logger.error('CSV parsing error', error);
            reject(error);
          }
        });
      });
    } catch (error) {
      logger.error(`Error reading CSV file: ${filePath}`, error);
      throw error;
    }
  }
}

module.exports = new CSVParser();

