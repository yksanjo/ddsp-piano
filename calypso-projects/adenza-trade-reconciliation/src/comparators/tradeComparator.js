const logger = require('../utils/logger');

class TradeComparator {
  compare(AdenzaTrades, externalTrades) {
    const discrepancies = [];
    const matchedExternalIds = new Set();

    // Normalize trade IDs for comparison
    const normalizeId = (id) => id.toString().trim().toUpperCase();

    // Create lookup maps
    const AdenzaMap = new Map();
    AdenzaTrades.forEach(trade => {
      const id = normalizeId(trade.id || trade.trade_id);
      AdenzaMap.set(id, trade);
    });

    const externalMap = new Map();
    externalTrades.forEach(trade => {
      const id = normalizeId(trade.trade_id || trade.id);
      externalMap.set(id, trade);
    });

    // Find trades in Adenza but not in external
    AdenzaMap.forEach((AdenzaTrade, id) => {
      if (!externalMap.has(id)) {
        discrepancies.push({
          type: 'missing_in_external',
          tradeId: id,
          Adenza: AdenzaTrade,
          external: null,
          fields: ['trade_id']
        });
      } else {
        matchedExternalIds.add(id);
        const externalTrade = externalMap.get(id);
        const fieldDiscrepancies = this.compareTradeFields(AdenzaTrade, externalTrade);
        
        if (fieldDiscrepancies.length > 0) {
          discrepancies.push({
            type: 'field_mismatch',
            tradeId: id,
            Adenza: AdenzaTrade,
            external: externalTrade,
            fields: fieldDiscrepancies
          });
        }
      }
    });

    // Find trades in external but not in Adenza
    externalMap.forEach((externalTrade, id) => {
      if (!AdenzaMap.has(id) && !matchedExternalIds.has(id)) {
        discrepancies.push({
          type: 'missing_in_Adenza',
          tradeId: id,
          Adenza: null,
          external: externalTrade,
          fields: ['trade_id']
        });
      }
    });

    logger.info(`Comparison complete: ${discrepancies.length} discrepancies found`);
    return discrepancies;
  }

  compareTradeFields(AdenzaTrade, externalTrade) {
    const discrepancies = [];
    const tolerance = 0.01; // For floating point comparisons

    // Compare notional
    const AdenzaNotional = parseFloat(AdenzaTrade.notional) || 0;
    const externalNotional = parseFloat(externalTrade.notional) || 0;
    if (Math.abs(AdenzaNotional - externalNotional) > tolerance) {
      discrepancies.push({
        field: 'notional',
        Adenza: AdenzaNotional,
        external: externalNotional
      });
    }

    // Compare trade date
    const AdenzaDate = this.normalizeDate(AdenzaTrade.tradeDate || AdenzaTrade.trade_date);
    const externalDate = this.normalizeDate(externalTrade.tradeDate || externalTrade.trade_date);
    if (AdenzaDate !== externalDate) {
      discrepancies.push({
        field: 'trade_date',
        Adenza: AdenzaDate,
        external: externalDate
      });
    }

    // Compare counterparty
    const AdenzaCpty = (AdenzaTrade.counterparty || '').trim().toUpperCase();
    const externalCpty = (externalTrade.counterparty || '').trim().toUpperCase();
    if (AdenzaCpty !== externalCpty) {
      discrepancies.push({
        field: 'counterparty',
        Adenza: AdenzaCpty,
        external: externalCpty
      });
    }

    // Compare instrument
    const AdenzaInst = (AdenzaTrade.instrument || '').trim().toUpperCase();
    const externalInst = (externalTrade.instrument || '').trim().toUpperCase();
    if (AdenzaInst !== externalInst) {
      discrepancies.push({
        field: 'instrument',
        Adenza: AdenzaInst,
        external: externalInst
      });
    }

    // Compare currency
    const AdenzaCurrency = (AdenzaTrade.currency || '').trim().toUpperCase();
    const externalCurrency = (externalTrade.currency || '').trim().toUpperCase();
    if (AdenzaCurrency && externalCurrency && AdenzaCurrency !== externalCurrency) {
      discrepancies.push({
        field: 'currency',
        Adenza: AdenzaCurrency,
        external: externalCurrency
      });
    }

    return discrepancies;
  }

  normalizeDate(dateStr) {
    if (!dateStr) return '';
    
    // Try to normalize various date formats
    const date = new Date(dateStr);
    if (isNaN(date.getTime())) return dateStr;
    
    return date.toISOString().split('T')[0]; // YYYY-MM-DD
  }
}

module.exports = new TradeComparator();

