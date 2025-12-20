const axios = require('axios');
const config = require('../config/config');
const mockRiskData = require('../mocks/riskData');

class RiskApiClient {
  constructor() {
    this.baseURL = config.calypso.apiBaseUrl;
    this.apiKey = config.calypso.apiKey;
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

  async getRiskData(filters = {}) {
    if (this.mockMode) {
      return mockRiskData;
    }

    try {
      const params = new URLSearchParams();
      if (filters.book) params.append('book', filters.book);
      if (filters.instrument) params.append('instrument', filters.instrument);
      if (filters.date) params.append('date', filters.date);

      const response = await axios.get(`${this.baseURL}/api/v1/risk`, {
        headers: this.getHeaders(),
        params: params
      });

      return response.data;
    } catch (error) {
      console.error('Error fetching risk data', error);
      throw error;
    }
  }

  async getGreeks(filters = {}) {
    if (this.mockMode) {
      return mockRiskData.map(d => ({
        instrument: d.instrument,
        book: d.book,
        delta: d.delta,
        gamma: d.gamma,
        vega: d.vega,
        theta: d.theta
      }));
    }

    try {
      const response = await axios.get(`${this.baseURL}/api/v1/risk/greeks`, {
        headers: this.getHeaders(),
        params: filters
      });

      return response.data;
    } catch (error) {
      console.error('Error fetching Greeks', error);
      throw error;
    }
  }
}

module.exports = new RiskApiClient();



