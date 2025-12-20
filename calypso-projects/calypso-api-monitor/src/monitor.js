const axios = require('axios');
const endpointConfig = require('./endpoints/endpointConfig');
const alertManager = require('./alerts/alertManager');
const metrics = require('./metrics/prometheus');
const logger = require('./utils/logger');

class Monitor {
  constructor() {
    this.endpoints = endpointConfig.getEndpoints();
    this.interval = null;
    this.metrics = [];
  }

  async checkEndpoint(endpoint) {
    const startTime = Date.now();
    
    try {
      const response = await axios.get(endpoint.url, {
        headers: endpoint.headers || {},
        timeout: endpoint.timeout || 5000
      });

      const latency = Date.now() - startTime;
      const status = response.status;

      // Record metrics
      metrics.recordLatency(endpoint.name, latency);
      metrics.recordStatus(endpoint.name, status);

      // Check for alerts
      if (latency > endpoint.threshold || endpoint.threshold === undefined && latency > 200) {
        await alertManager.triggerAlert({
          endpoint: endpoint.name,
          latency: latency,
          threshold: endpoint.threshold || 200,
          status: status
        });
      }

      return {
        endpoint: endpoint.name,
        status: 'OK',
        latency: latency,
        httpStatus: status,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      const latency = Date.now() - startTime;
      
      metrics.recordLatency(endpoint.name, latency);
      metrics.recordError(endpoint.name);

      await alertManager.triggerAlert({
        endpoint: endpoint.name,
        latency: latency,
        error: error.message,
        status: 'ERROR'
      });

      return {
        endpoint: endpoint.name,
        status: 'ERROR',
        latency: latency,
        error: error.message,
        timestamp: new Date().toISOString()
      };
    }
  }

  async checkAll() {
    logger.info('Checking all endpoints...');
    const results = await Promise.all(
      this.endpoints.map(endpoint => this.checkEndpoint(endpoint))
    );
    
    this.metrics.push({
      timestamp: new Date().toISOString(),
      results: results
    });

    return results;
  }

  start(intervalMs = 60000) {
    logger.info(`Starting monitor with ${intervalMs}ms interval`);
    this.checkAll(); // Run immediately
    
    this.interval = setInterval(() => {
      this.checkAll();
    }, intervalMs);
  }

  stop() {
    if (this.interval) {
      clearInterval(this.interval);
      this.interval = null;
      logger.info('Monitor stopped');
    }
  }
}

module.exports = new Monitor();



