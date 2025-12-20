class BookValidator {
  validate(book) {
    const errors = [];

    // Check for required fields
    if (!book.id && !book.name) {
      errors.push('Missing ID or name');
    }

    // Check for legal entity reference
    if (!book.legalEntityId && !book.legalEntity) {
      errors.push('Missing legal entity reference');
    }

    // Check for currency
    if (!book.baseCurrency) {
      errors.push('Missing base currency');
    } else if (!this.isValidCurrency(book.baseCurrency)) {
      errors.push(`Invalid currency code: ${book.baseCurrency}`);
    }

    // Check for book type
    if (!book.type) {
      errors.push('Missing book type');
    }

    return {
      valid: errors.length === 0,
      errors: errors
    };
  }

  isValidCurrency(currency) {
    // ISO 4217 currency codes are 3 letters
    const currencyRegex = /^[A-Z]{3}$/;
    return currencyRegex.test(currency);
  }
}

module.exports = new BookValidator();



