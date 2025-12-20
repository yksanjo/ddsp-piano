require('dotenv').config();

module.exports = {
  Adenza: {
    apiBaseUrl: process.env.ADENZA_API_BASE_URL || 'https://adenza-api.example.com',
    apiKey: process.env.ADENZA_API_KEY || '',
    apiSecret: process.env.ADENZA_API_SECRET || '',
    authType: process.env.AUTH_TYPE || 'api_key',
    oauth: {
      clientId: process.env.OAUTH_CLIENT_ID || '',
      clientSecret: process.env.OAUTH_CLIENT_SECRET || '',
      tokenUrl: process.env.OAUTH_TOKEN_URL || ''
    }
  },
  server: {
    port: parseInt(process.env.PORT || '3001', 10),
    wsPort: parseInt(process.env.WS_PORT || '3002', 10),
    nodeEnv: process.env.NODE_ENV || 'development'
  },
  mockMode: process.env.MOCK_MODE === 'true',
  logging: {
    level: process.env.LOG_LEVEL || 'info'
  }
};

