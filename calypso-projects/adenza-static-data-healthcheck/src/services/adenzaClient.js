const axios = require('axios');
const config = require('../config/config');
const logger = require('../utils/logger');
const mockData = require('../mocks/staticData');

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

  async getLegalEntities() {
    if (this.mockMode) {
      return mockData.legalEntities;
    }

    try {
      const response = await axios.get(`${this.baseURL}/api/v1/legal-entities`, {
        headers: this.getHeaders()
      });
      return response.data;
    } catch (error) {
      logger.error('Error fetching legal entities', error);
      throw error;
    }
  }

  async getBooks() {
    if (this.mockMode) {
      return mockData.books;
    }

    try {
      const response = await axios.get(`${this.baseURL}/api/v1/books`, {
        headers: this.getHeaders()
      });
      return response.data;
    } catch (error) {
      logger.error('Error fetching books', error);
      throw error;
    }
  }

  async getPortfolios() {
    if (this.mockMode) {
      return mockData.portfolios;
    }

    try {
      const response = await axios.get(`${this.baseURL}/api/v1/portfolios`, {
        headers: this.getHeaders()
      });
      return response.data;
    } catch (error) {
      logger.error('Error fetching portfolios', error);
      throw error;
    }
  }
}

module.exports = new AdenzaClient();

