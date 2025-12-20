const fs = require('fs');
const logger = require('../utils/logger');

class SWIFTParser {
  async parse(filePath) {
    try {
      const fileContent = fs.readFileSync(filePath, 'utf8');
      const messages = this.splitSWIFTMessages(fileContent);
      
      const trades = messages.map((message, index) => {
        const parsed = this.parseSWIFTMessage(message);
        return {
          trade_id: parsed.tradeId || `SWIFT-${index + 1}`,
          trade_date: parsed.tradeDate,
          counterparty: parsed.counterparty,
          instrument: parsed.instrument,
          notional: parsed.notional,
          currency: parsed.currency,
          status: parsed.status || 'Confirmed',
          source: 'swift',
          messageType: parsed.messageType
        };
      });

      logger.info(`Parsed ${trades.length} trades from SWIFT messages`);
      return trades;
    } catch (error) {
      logger.error(`Error parsing SWIFT file: ${filePath}`, error);
      throw error;
    }
  }

  splitSWIFTMessages(content) {
    // SWIFT messages start with {1: and end with -}
    const messages = [];
    let currentMessage = '';
    let inMessage = false;

    for (let i = 0; i < content.length; i++) {
      if (content.substring(i, i + 2) === '{1:') {
        inMessage = true;
        currentMessage = '{1:';
        i += 1;
      } else if (inMessage) {
        currentMessage += content[i];
        if (content[i] === '}' && currentMessage.endsWith('-}')) {
          messages.push(currentMessage);
          currentMessage = '';
          inMessage = false;
        }
      }
    }

    return messages;
  }

  parseSWIFTMessage(message) {
    const result = {
      messageType: null,
      tradeId: null,
      tradeDate: null,
      counterparty: null,
      instrument: null,
      notional: null,
      currency: null
    };

    // Extract message type (MT103, MT300, etc.)
    const mtMatch = message.match(/MT(\d{3})/);
    if (mtMatch) {
      result.messageType = `MT${mtMatch[1]}`;
    }

    // MT103 parsing (Payment message)
    if (result.messageType === 'MT103') {
      // Extract trade date (field 30)
      const dateMatch = message.match(/30:(\d{6})/);
      if (dateMatch) {
        const dateStr = dateMatch[1];
        result.tradeDate = `20${dateStr.substring(0, 2)}-${dateStr.substring(2, 4)}-${dateStr.substring(4, 6)}`;
      }

      // Extract amount (field 32A)
      const amountMatch = message.match(/32A:(\d{6})([A-Z]{3})([\d,]+)/);
      if (amountMatch) {
        result.currency = amountMatch[2];
        result.notional = parseFloat(amountMatch[3].replace(/,/g, ''));
      }

      // Extract counterparty (field 50A or 50K)
      const cptyMatch = message.match(/50[AK]:([A-Z0-9]+)/);
      if (cptyMatch) {
        result.counterparty = cptyMatch[1];
      }
    }

    // MT300 parsing (Foreign Exchange Confirmation)
    if (result.messageType === 'MT300') {
      // Extract trade date
      const dateMatch = message.match(/30T:(\d{8})/);
      if (dateMatch) {
        const dateStr = dateMatch[1];
        result.tradeDate = `${dateStr.substring(0, 4)}-${dateStr.substring(4, 6)}-${dateStr.substring(6, 8)}`;
      }

      // Extract currencies and amounts
      const buyMatch = message.match(/33B:([A-Z]{3})([\d,]+)/);
      const sellMatch = message.match(/53B:([A-Z]{3})([\d,]+)/);
      
      if (buyMatch && sellMatch) {
        result.instrument = `${buyMatch[1]}/${sellMatch[1]}`;
        result.notional = parseFloat(buyMatch[2].replace(/,/g, ''));
        result.currency = buyMatch[1];
      }

      // Extract counterparty
      const cptyMatch = message.match(/50[AK]:([A-Z0-9]+)/);
      if (cptyMatch) {
        result.counterparty = cptyMatch[1];
      }
    }

    return result;
  }
}

module.exports = new SWIFTParser();



