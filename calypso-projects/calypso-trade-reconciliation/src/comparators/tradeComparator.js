const logger = require('../utils/logger');

class TradeComparator {
  compare(calypsoTrades, externalTrades) {
    const discrepancies = [];
    const matchedExternalIds = new Set();

    // Normalize trade IDs for comparison
    const normalizeId = (id) => id.toString().trim().toUpperCase();

    // Create lookup maps
    const calypsoMap = new Map();
    calypsoTrades.forEach(trade => {
      const id = normalizeId(trade.id || trade.trade_id);
      calypsoMap.set(id, trade);
    });

    const externalMap = new Map();
    externalTrades.forEach(trade => {
      const id = normalizeId(trade.trade_id || trade.id);
      externalMap.set(id, trade);
    });

    // Find trades in Calypso but not in external
    calypsoMap.forEach((calypsoTrade, id) => {
      if (!externalMap.has(id)) {
        discrepancies.push({
          type: 'missing_in_external',
          tradeId: id,
          calypso: calypsoTrade,
          external: null,
          fields: ['trade_id']
        });
      } else {
        matchedExternalIds.add(id);
        const externalTrade = externalMap.get(id);
        const fieldDiscrepancies = this.compareTradeFields(calypsoTrade, externalTrade);
        
        if (fieldDiscrepancies.length > 0) {
          discrepancies.push({
            type: 'field_mismatch',
            tradeId: id,
            calypso: calypsoTrade,
            external: externalTrade,
            fields: fieldDiscrepancies
          });
        }
      }
    });

    // Find trades in external but not in Calypso
    externalMap.forEach((externalTrade, id) => {
      if (!calypsoMap.has(id) && !matchedExternalIds.has(id)) {
        discrepancies.push({
          type: 'missing_in_calypso',
          tradeId: id,
          calypso: null,
          external: externalTrade,
          fields: ['trade_id']
        });
      }
    });

    logger.info(`Comparison complete: ${discrepancies.length} discrepancies found`);
    return discrepancies;
  }

  compareTradeFields(calypsoTrade, externalTrade) {
    const discrepancies = [];
    const tolerance = 0.01; // For floating point comparisons

    // Compare notional
    const calypsoNotional = parseFloat(calypsoTrade.notional) || 0;
    const externalNotional = parseFloat(externalTrade.notional) || 0;
    if (Math.abs(calypsoNotional - externalNotional) > tolerance) {
      discrepancies.push({
        field: 'notional',
        calypso: calypsoNotional,
        external: externalNotional
      });
    }

    // Compare trade date
    const calypsoDate = this.normalizeDate(calypsoTrade.tradeDate || calypsoTrade.trade_date);
    const externalDate = this.normalizeDate(externalTrade.tradeDate || externalTrade.trade_date);
    if (calypsoDate !== externalDate) {
      discrepancies.push({
        field: 'trade_date',
        calypso: calypsoDate,
        external: externalDate
      });
    }

    // Compare counterparty
    const calypsoCpty = (calypsoTrade.counterparty || '').trim().toUpperCase();
    const externalCpty = (externalTrade.counterparty || '').trim().toUpperCase();
    if (calypsoCpty !== externalCpty) {
      discrepancies.push({
        field: 'counterparty',
        calypso: calypsoCpty,
        external: externalCpty
      });
    }

    // Compare instrument
    const calypsoInst = (calypsoTrade.instrument || '').trim().toUpperCase();
    const externalInst = (externalTrade.instrument || '').trim().toUpperCase();
    if (calypsoInst !== externalInst) {
      discrepancies.push({
        field: 'instrument',
        calypso: calypsoInst,
        external: externalInst
      });
    }

    // Compare currency
    const calypsoCurrency = (calypsoTrade.currency || '').trim().toUpperCase();
    const externalCurrency = (externalTrade.currency || '').trim().toUpperCase();
    if (calypsoCurrency && externalCurrency && calypsoCurrency !== externalCurrency) {
      discrepancies.push({
        field: 'currency',
        calypso: calypsoCurrency,
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



