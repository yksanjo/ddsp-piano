const mt103Template = require('./templates/mt103');
const mt300Template = require('./templates/mt300');
const swiftValidator = require('./validators/swiftValidator');
const logger = require('./utils/logger');

class SWIFTGenerator {
  generate(tradeData, messageType = 'MT103') {
    let message;

    switch (messageType) {
      case 'MT103':
        message = mt103Template.generate(tradeData);
        break;
      case 'MT300':
        message = mt300Template.generate(tradeData);
        break;
      default:
        throw new Error(`Unsupported message type: ${messageType}`);
    }

    // Validate the generated message
    const validation = swiftValidator.validate(message, messageType);
    if (!validation.valid) {
      logger.warn('Generated SWIFT message validation warnings', validation.errors);
    }

    return {
      message: message,
      messageType: messageType,
      valid: validation.valid,
      errors: validation.errors
    };
  }

  generateBatch(trades, messageType = 'MT103') {
    return trades.map(trade => this.generate(trade, messageType));
  }
}

module.exports = new SWIFTGenerator();



