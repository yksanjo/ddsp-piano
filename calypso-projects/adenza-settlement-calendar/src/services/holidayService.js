const axios = require('axios');
const config = require('../config/config');
const mockHolidays = require('../mocks/holidays');

class HolidayService {
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

  async getHolidays(currencyPair) {
    if (this.mockMode) {
      return mockHolidays[currencyPair] || [];
    }

    try {
      const [baseCurrency, quoteCurrency] = currencyPair.split('/');
      const response = await axios.get(`${this.baseURL}/api/v1/holidays`, {
        headers: this.getHeaders(),
        params: {
          baseCurrency,
          quoteCurrency
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching holidays', error);
      throw error;
    }
  }
}

module.exports = new HolidayService();

