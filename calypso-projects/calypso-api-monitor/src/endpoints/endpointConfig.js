const config = require('../config/config');

class EndpointConfig {
  getEndpoints() {
    if (config.mockMode) {
      return [
        {
          name: 'Price Discovery',
          url: 'https://calypso-api.example.com/api/v1/prices',
          threshold: 200,
          timeout: 5000
        },
        {
          name: 'Trade Status',
          url: 'https://calypso-api.example.com/api/v1/trades',
          threshold: 200,
          timeout: 5000
        },
        {
          name: 'Risk Data',
          url: 'https://calypso-api.example.com/api/v1/risk',
          threshold: 300,
          timeout: 5000
        }
      ];
    }

    // Load from environment or config file
    return config.endpoints || [];
  }
}

module.exports = new EndpointConfig();



