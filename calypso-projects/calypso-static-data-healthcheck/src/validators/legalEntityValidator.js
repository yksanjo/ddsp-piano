class LegalEntityValidator {
  validate(entity) {
    const errors = [];

    // Check for required fields
    if (!entity.id && !entity.name) {
      errors.push('Missing ID or name');
    }

    // Check for LEI code
    if (!entity.lei) {
      errors.push('Missing LEI (Legal Entity Identifier) code');
    } else if (!this.isValidLEI(entity.lei)) {
      errors.push(`Invalid LEI format: ${entity.lei}`);
    }

    // Check for country code
    if (!entity.country) {
      errors.push('Missing country code');
    }

    // Check for legal name
    if (!entity.legalName) {
      errors.push('Missing legal name');
    }

    return {
      valid: errors.length === 0,
      errors: errors
    };
  }

  isValidLEI(lei) {
    // LEI format: 20 alphanumeric characters
    const leiRegex = /^[A-Z0-9]{20}$/;
    return leiRegex.test(lei);
  }
}

module.exports = new LegalEntityValidator();



