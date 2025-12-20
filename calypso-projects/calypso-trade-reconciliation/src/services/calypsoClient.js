const axios = require('axios');
const config = require('../config/config');
const logger = require('../utils/logger');
const mockTrades = require('../mocks/trades');

class CalypsoClient {
  constructor() {
    this.baseURL = config.calypso.apiBaseUrl;
    this.apiKey = config.calypso.apiKey;
    this.apiSecret = config.calypso.apiSecret;
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
    headers['X-API-Secret'] = this.apiSecret;

    return headers;
  }

  async getTrades(filters = {}) {
    if (this.mockMode) {
      logger.info('Mock mode: Returning mock trades');
      return mockTrades;
    }

    try {
      const params = new URLSearchParams();
      if (filters.startDate) params.append('startDate', filters.startDate);
      if (filters.endDate) params.append('endDate', filters.endDate);

      const response = await axios.get(`${this.baseURL}/api/v1/trades`, {
        headers: this.getHeaders(),
        params: params
      });

      return response.data;
    } catch (error) {
      logger.error('Error fetching trades from Calypso API', error);
      throw error;
    }
  }
}

module.exports = new CalypsoClient();



