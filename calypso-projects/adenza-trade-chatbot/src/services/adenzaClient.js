const axios = require('axios');
const config = require('../config/config');
const logger = require('../utils/logger');
const mockData = require('../mocks/data');

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

  async executeQuery(apiCall) {
    if (this.mockMode) {
      logger.info('Mock mode: Returning mock data');
      return mockData[apiCall.endpoint] || [];
    }

    try {
      const response = await axios({
        method: apiCall.method || 'GET',
        url: `${this.baseURL}${apiCall.endpoint}`,
        headers: this.getHeaders(),
        params: apiCall.params || {}
      });

      return response.data;
    } catch (error) {
      logger.error('Error executing API call', error);
      throw error;
    }
  }
}

module.exports = new AdenzaClient();

