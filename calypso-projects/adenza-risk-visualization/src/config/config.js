require('dotenv').config();

module.exports = {
  Adenza: {
    apiBaseUrl: process.env.ADENZA_API_BASE_URL || 'https://adenza-api.example.com',
    apiKey: process.env.ADENZA_API_KEY || ''
  },
  mockMode: process.env.MOCK_MODE === 'true'
};

