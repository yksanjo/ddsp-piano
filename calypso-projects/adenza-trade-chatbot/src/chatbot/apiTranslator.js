class APITranslator {
  translate(parsedQuery) {
    const { intent, entities } = parsedQuery;

    const apiCall = {
      endpoint: this.getEndpoint(intent),
      method: 'GET',
      params: {}
    };

    // Add filters based on entities
    if (entities.counterparty) {
      apiCall.params.counterparty = entities.counterparty;
    }

    if (entities.date) {
      apiCall.params.date = this.parseDate(entities.date);
    }

    if (entities.currencyPair) {
      apiCall.params.currencyPair = entities.currencyPair;
    }

    if (entities.book) {
      apiCall.params.book = entities.book;
    }

    return apiCall;
  }

  getEndpoint(intent) {
    const endpoints = {
      'exposure': '/api/v1/exposure',
      'trades': '/api/v1/trades',
      'positions': '/api/v1/positions',
      'pricing': '/api/v1/prices',
      'general': '/api/v1/search'
    };

    return endpoints[intent] || endpoints['general'];
  }

  parseDate(dateString) {
    // Simple date parsing - can be enhanced
    const months = {
      'january': '01', 'february': '02', 'march': '03',
      'april': '04', 'may': '05', 'june': '06',
      'july': '07', 'august': '08', 'september': '09',
      'october': '10', 'november': '11', 'december': '12'
    };

    const parts = dateString.toLowerCase().split(' ');
    if (parts.length === 2) {
      const month = months[parts[0]];
      const year = parts[1];
      return `${year}-${month}-01`;
    }

    return new Date().toISOString().split('T')[0];
  }
}

module.exports = new APITranslator();

