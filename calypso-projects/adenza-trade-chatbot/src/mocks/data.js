module.exports = {
  '/api/v1/exposure': [
    { counterparty: 'Deutsche Bank', exposure: 5000000, currency: 'USD' },
    { counterparty: 'JP Morgan', exposure: 3000000, currency: 'USD' }
  ],
  '/api/v1/trades': [
    { id: 'TRD-001', counterparty: 'Deutsche Bank', notional: 1000000, status: 'Confirmed' },
    { id: 'TRD-002', counterparty: 'JP Morgan', notional: 500000, status: 'Pending' }
  ],
  '/api/v1/positions': [
    { instrument: 'USD/EUR', quantity: 1000000, book: 'Trading-Book-1' }
  ],
  '/api/v1/prices': [
    { instrument: 'USD/EUR', bid: 1.0850, ask: 1.0852 }
  ]
};

