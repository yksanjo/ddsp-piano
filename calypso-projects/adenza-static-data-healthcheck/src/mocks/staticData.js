module.exports = {
  legalEntities: [
    {
      id: 'LE-001',
      name: 'Entity 1',
      lei: '12345678901234567890',
      country: 'US',
      legalName: 'Legal Entity 1'
    },
    {
      id: 'LE-002',
      name: 'Entity 2',
      // Missing LEI
      country: 'GB',
      legalName: 'Legal Entity 2'
    }
  ],
  books: [
    {
      id: 'BOOK-001',
      name: 'Trading Book 1',
      legalEntityId: 'LE-001',
      baseCurrency: 'USD',
      type: 'Trading'
    },
    {
      id: 'BOOK-002',
      name: 'Trading Book 2',
      // Missing legal entity
      baseCurrency: 'EUR',
      type: 'Trading'
    }
  ],
  portfolios: [
    {
      id: 'PORT-001',
      name: 'Portfolio 1',
      bookId: 'BOOK-001',
      type: 'Trading'
    },
    {
      id: 'PORT-002',
      name: 'Portfolio 2',
      // Missing book
      type: 'Trading'
    }
  ]
};

