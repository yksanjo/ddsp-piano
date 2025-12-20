require('dotenv').config();

module.exports = {
  calypso: {
    apiBaseUrl: process.env.CALYPSO_API_BASE_URL || 'https://calypso-api.example.com',
    apiKey: process.env.CALYPSO_API_KEY || ''
  },
  mockMode: process.env.MOCK_MODE === 'true'
};



