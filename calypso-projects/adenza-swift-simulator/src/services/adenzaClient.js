const axios = require('axios');
const config = require('../config/config');
const logger = require('../utils/logger');

class AdenzaClient {
  constructor() {
    this.baseURL = config.Adenza.apiBaseUrl;
    this.apiKey = config.Adenza.apiKey;
    this.mockMode = config.mockMode;
  }

  getHeaders() {
    const headers = {
      'Content-Type': 'application/json'
    };

    if (this.mockMode) {
      return headers;
    }

    headers['X-API-Key'] = this.apiKey;
    return headers;
  }

  async getTradeById(tradeId) {
    if (this.mockMode) {
      logger.info('Mock mode: Returning null (trade not found)');
      return null;
    }

    try {
      const response = await axios.get(`${this.baseURL}/api/v1/trades/${tradeId}`, {
        headers: this.getHeaders()
      });
      return response.data;
    } catch (error) {
      logger.error(`Error fetching trade ${tradeId}`, error);
      throw error;
    }
  }
}

module.exports = new AdenzaClient();

