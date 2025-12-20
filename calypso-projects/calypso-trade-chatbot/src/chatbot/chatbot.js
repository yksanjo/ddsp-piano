const queryParser = require('./queryParser');
const apiTranslator = require('./apiTranslator');
const llmService = require('../services/llmService');
const calypsoClient = require('../services/calypsoClient');
const logger = require('../utils/logger');

class Chatbot {
  constructor() {
    this.conversationHistory = [];
  }

  async processQuery(userQuery) {
    try {
      logger.info(`Processing query: ${userQuery}`);

      // Parse the query to extract intent and entities
      const parsedQuery = queryParser.parse(userQuery);

      // Translate to API call
      const apiCall = apiTranslator.translate(parsedQuery);

      // Execute API call
      const data = await calypsoClient.executeQuery(apiCall);

      // Generate natural language response using LLM
      const response = await llmService.generateResponse(userQuery, data, parsedQuery);

      // Store in history
      this.conversationHistory.push({
        query: userQuery,
        response: response,
        timestamp: new Date().toISOString()
      });

      return response;
    } catch (error) {
      logger.error('Error processing query', error);
      return `I'm sorry, I encountered an error processing your query: ${error.message}`;
    }
  }

  getHistory() {
    return this.conversationHistory;
  }

  clearHistory() {
    this.conversationHistory = [];
  }
}

module.exports = new Chatbot();



