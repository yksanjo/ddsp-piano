const axios = require('axios');
const config = require('../config/config');
const logger = require('../utils/logger');
const mockTrades = require('../mocks/trades');

class AdenzaClient {
  constructor() {
    this.baseURL = config.Adenza.apiBaseUrl;
    this.apiKey = config.Adenza.apiKey;
    this.apiSecret = config.Adenza.apiSecret;
    this.authType = config.Adenza.authType;
    this.mockMode = config.mockMode;
    this.accessToken = null;
  }

  async authenticate() {
    if (this.mockMode) {
      logger.info('Mock mode: Skipping authentication');
      return true;
    }

    if (this.authType === 'oauth2') {
      try {
        const response = await axios.post(config.Adenza.oauth.tokenUrl, {
          client_id: config.Adenza.oauth.clientId,
          client_secret: config.Adenza.oauth.clientSecret,
          grant_type: 'client_credentials'
        });
        this.accessToken = response.data.access_token;
        logger.info('OAuth2 authentication successful');
        return true;
      } catch (error) {
        logger.error('OAuth2 authentication failed', error);
        throw error;
      }
    }
    return true;
  }

  getHeaders() {
    const headers = {
      'Content-Type': 'application/json'
    };

    if (this.mockMode) {
      return headers;
    }

    if (this.authType === 'oauth2' && this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`;
    } else if (this.authType === 'api_key') {
      headers['X-API-Key'] = this.apiKey;
      headers['X-API-Secret'] = this.apiSecret;
    }

    return headers;
  }

  async getTrades(filters = {}) {
    if (this.mockMode) {
      logger.info('Mock mode: Returning mock trades');
      return this.filterMockTrades(mockTrades, filters);
    }

    try {
      const params = new URLSearchParams();
      if (filters.book) params.append('book', filters.book);
      if (filters.counterparty) params.append('counterparty', filters.counterparty);
      if (filters.startDate) params.append('startDate', filters.startDate);
      if (filters.endDate) params.append('endDate', filters.endDate);
      if (filters.status) params.append('status', filters.status);

      const response = await axios.get(`${this.baseURL}/api/v1/trades`, {
        headers: this.getHeaders(),
        params: params
      });

      return response.data;
    } catch (error) {
      logger.error('Error fetching trades from Adenza API', error);
      throw error;
    }
  }

  async getTradeById(tradeId) {
    if (this.mockMode) {
      logger.info('Mock mode: Returning mock trade');
      const trade = mockTrades.find(t => t.id === tradeId);
      return trade || null;
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

  filterMockTrades(trades, filters) {
    let filtered = [...trades];

    if (filters.book) {
      filtered = filtered.filter(t => t.book === filters.book);
    }
    if (filters.counterparty) {
      filtered = filtered.filter(t => t.counterparty === filters.counterparty);
    }
    if (filters.status) {
      filtered = filtered.filter(t => t.status === filters.status);
    }
    if (filters.startDate) {
      filtered = filtered.filter(t => new Date(t.tradeDate) >= new Date(filters.startDate));
    }
    if (filters.endDate) {
      filtered = filtered.filter(t => new Date(t.tradeDate) <= new Date(filters.endDate));
    }

    return filtered;
  }
}

module.exports = new AdenzaClient();

