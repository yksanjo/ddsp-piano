class SWIFTValidator {
  validate(message, messageType) {
    const errors = [];

    // Basic structure validation
    if (!message.includes('{1:')) {
      errors.push('Missing block 1');
    }

    if (!message.includes('{2:')) {
      errors.push('Missing block 2');
    }

    if (!message.includes('{4:')) {
      errors.push('Missing block 4');
    }

    if (!message.includes('{5:')) {
      errors.push('Missing block 5');
    }

    // Message type specific validation
    if (messageType === 'MT103') {
      if (!message.includes(':20:')) {
        errors.push('MT103: Missing field 20 (Transaction Reference)');
      }
      if (!message.includes(':32A:')) {
        errors.push('MT103: Missing field 32A (Value Date, Currency Code, Amount)');
      }
    }

    if (messageType === 'MT300') {
      if (!message.includes(':20:')) {
        errors.push('MT300: Missing field 20 (Transaction Reference)');
      }
      if (!message.includes(':32B:')) {
        errors.push('MT300: Missing field 32B (Currency Code, Amount)');
      }
      if (!message.includes(':33B:')) {
        errors.push('MT300: Missing field 33B (Currency Code, Amount)');
      }
    }

    // Check for balanced braces
    const openBraces = (message.match(/{/g) || []).length;
    const closeBraces = (message.match(/}/g) || []).length;
    if (openBraces !== closeBraces) {
      errors.push('Unbalanced braces in message');
    }

    return {
      valid: errors.length === 0,
      errors: errors
    };
  }
}

module.exports = new SWIFTValidator();

