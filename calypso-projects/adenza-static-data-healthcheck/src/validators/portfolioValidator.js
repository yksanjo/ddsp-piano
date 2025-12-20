class PortfolioValidator {
  validate(portfolio) {
    const errors = [];

    // Check for required fields
    if (!portfolio.id && !portfolio.name) {
      errors.push('Missing ID or name');
    }

    // Check for book reference
    if (!portfolio.bookId && !portfolio.book) {
      errors.push('Missing book reference');
    }

    // Check for portfolio type
    if (!portfolio.type) {
      errors.push('Missing portfolio type');
    }

    return {
      valid: errors.length === 0,
      errors: errors
    };
  }
}

module.exports = new PortfolioValidator();

