require('dotenv').config();

module.exports = {
  Adenza: {
    apiBaseUrl: process.env.ADENZA_API_BASE_URL || 'https://adenza-api.example.com',
    apiKey: process.env.ADENZA_API_KEY || ''
  },
  mockMode: process.env.MOCK_MODE === 'true',
  monitor: {
    interval: parseInt(process.env.MONITOR_INTERVAL || '60000', 10)
  },
  server: {
    port: parseInt(process.env.PORT || '3000', 10)
  },
  alerts: {
    email: {
      enabled: process.env.EMAIL_ALERTS_ENABLED === 'true'
    },
    slack: {
      enabled: process.env.SLACK_ALERTS_ENABLED === 'true',
      webhookUrl: process.env.SLACK_WEBHOOK_URL || ''
    }
  },
  endpoints: process.env.ENDPOINTS ? JSON.parse(process.env.ENDPOINTS) : []
};

