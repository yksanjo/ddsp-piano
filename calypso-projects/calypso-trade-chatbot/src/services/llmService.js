const { ChatOpenAI } = require('@langchain/openai');
const config = require('../config/config');
const logger = require('../utils/logger');

class LLMService {
  constructor() {
    if (config.llm.provider === 'openai' && config.llm.openai.apiKey) {
      this.llm = new ChatOpenAI({
        openAIApiKey: config.llm.openai.apiKey,
        modelName: config.llm.openai.model || 'gpt-3.5-turbo',
        temperature: 0.7
      });
    } else {
      logger.warn('LLM not configured, using mock responses');
      this.llm = null;
    }
  }

  async generateResponse(userQuery, data, parsedQuery) {
    if (!this.llm) {
      return this.generateMockResponse(userQuery, data, parsedQuery);
    }

    try {
      const prompt = this.buildPrompt(userQuery, data, parsedQuery);
      const response = await this.llm.invoke(prompt);
      return response.content;
    } catch (error) {
      logger.error('LLM error', error);
      return this.generateMockResponse(userQuery, data, parsedQuery);
    }
  }

  buildPrompt(userQuery, data, parsedQuery) {
    return `You are a helpful assistant for a Calypso trading platform. 
    
User Query: ${userQuery}

Query Intent: ${parsedQuery.intent}
Extracted Entities: ${JSON.stringify(parsedQuery.entities)}

Data Retrieved: ${JSON.stringify(data, null, 2)}

Please provide a clear, concise, and professional response to the user's query based on the data provided. 
If the data is empty or null, indicate that no matching records were found.`;
  }

  generateMockResponse(userQuery, data, parsedQuery) {
    if (!data || (Array.isArray(data) && data.length === 0)) {
      return `I couldn't find any data matching your query: "${userQuery}". Please try rephrasing your question.`;
    }

    if (parsedQuery.intent === 'exposure') {
      const total = Array.isArray(data) ? data.reduce((sum, d) => sum + (d.exposure || 0), 0) : data.exposure || 0;
      return `Based on your query, the total exposure is ${total.toLocaleString()}.`;
    }

    if (parsedQuery.intent === 'trades') {
      const count = Array.isArray(data) ? data.length : 1;
      return `I found ${count} trade(s) matching your query.`;
    }

    return `Here's the information I found: ${JSON.stringify(data, null, 2)}`;
  }
}

module.exports = new LLMService();



