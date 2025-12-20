require('dotenv').config();

module.exports = {
  Adenza: {
    apiBaseUrl: process.env.ADENZA_API_BASE_URL || 'https://adenza-api.example.com',
    apiKey: process.env.ADENZA_API_KEY || ''
  },
  mockMode: process.env.MOCK_MODE === 'true',
  llm: {
    provider: process.env.LLM_PROVIDER || 'openai',
    openai: {
      apiKey: process.env.OPENAI_API_KEY || '',
      model: process.env.OPENAI_MODEL || 'gpt-3.5-turbo'
    }
  },
  server: {
    port: parseInt(process.env.PORT || '3000', 10)
  }
};

