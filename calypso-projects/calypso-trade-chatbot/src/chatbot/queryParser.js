class QueryParser {
  parse(query) {
    const normalizedQuery = query.toLowerCase().trim();

    // Extract intent
    const intent = this.extractIntent(normalizedQuery);

    // Extract entities
    const entities = this.extractEntities(normalizedQuery);

    return {
      intent: intent,
      entities: entities,
      originalQuery: query
    };
  }

  extractIntent(query) {
    if (query.includes('exposure') || query.includes('risk')) {
      return 'exposure';
    }
    if (query.includes('trade') || query.includes('transaction')) {
      return 'trades';
    }
    if (query.includes('position') || query.includes('holding')) {
      return 'positions';
    }
    if (query.includes('price') || query.includes('rate')) {
      return 'pricing';
    }
    return 'general';
  }

  extractEntities(query) {
    const entities = {};

    // Extract counterparty
    const counterpartyPatterns = ['deutsche bank', 'jp morgan', 'goldman sachs', 'morgan stanley', 'barclays'];
    counterpartyPatterns.forEach(cpty => {
      if (query.includes(cpty)) {
        entities.counterparty = cpty;
      }
    });

    // Extract date
    const datePattern = /(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{4})/i;
    const dateMatch = query.match(datePattern);
    if (dateMatch) {
      entities.date = dateMatch[0];
    }

    // Extract currency pair
    const currencyPattern = /([a-z]{3})\/([a-z]{3})/i;
    const currencyMatch = query.match(currencyPattern);
    if (currencyMatch) {
      entities.currencyPair = currencyMatch[0].toUpperCase();
    }

    // Extract book
    const bookPattern = /book\s+([a-z0-9-]+)/i;
    const bookMatch = query.match(bookPattern);
    if (bookMatch) {
      entities.book = bookMatch[1];
    }

    return entities;
  }
}

module.exports = new QueryParser();



