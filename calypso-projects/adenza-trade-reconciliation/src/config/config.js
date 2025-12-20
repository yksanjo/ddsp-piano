require('dotenv').config();

module.exports = {
  Adenza: {
    apiBaseUrl: process.env.ADENZA_API_BASE_URL || 'https://adenza-api.example.com',
    apiKey: process.env.ADENZA_API_KEY || '',
    apiSecret: process.env.ADENZA_API_SECRET || ''
  },
  mockMode: process.env.MOCK_MODE === 'true',
  email: {
    enabled: process.env.EMAIL_ENABLED === 'true',
    smtp: {
      host: process.env.SMTP_HOST || 'smtp.gmail.com',
      port: parseInt(process.env.SMTP_PORT || '587', 10),
      secure: process.env.SMTP_SECURE === 'true',
      user: process.env.SMTP_USER || '',
      password: process.env.SMTP_PASSWORD || ''
    },
    to: process.env.EMAIL_TO || '',
    from: process.env.EMAIL_FROM || ''
  },
  logging: {
    level: process.env.LOG_LEVEL || 'info'
  }
};

