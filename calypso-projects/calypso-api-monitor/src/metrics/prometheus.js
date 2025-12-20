const client = require('prom-client');

// Create a Registry to register the metrics
const register = new client.Registry();

// Add default metrics
client.collectDefaultMetrics({ register });

// Custom metrics
const latencyHistogram = new client.Histogram({
  name: 'calypso_api_latency_seconds',
  help: 'API endpoint latency in seconds',
  labelNames: ['endpoint'],
  buckets: [0.1, 0.2, 0.5, 1, 2, 5]
});

const statusCounter = new client.Counter({
  name: 'calypso_api_requests_total',
  help: 'Total number of API requests',
  labelNames: ['endpoint', 'status']
});

const errorCounter = new client.Counter({
  name: 'calypso_api_errors_total',
  help: 'Total number of API errors',
  labelNames: ['endpoint']
});

register.registerMetric(latencyHistogram);
register.registerMetric(statusCounter);
register.registerMetric(errorCounter);

class Metrics {
  recordLatency(endpoint, latencyMs) {
    latencyHistogram.observe({ endpoint }, latencyMs / 1000);
  }

  recordStatus(endpoint, status) {
    statusCounter.inc({ endpoint, status: status.toString() });
  }

  recordError(endpoint) {
    errorCounter.inc({ endpoint });
  }

  async getMetrics() {
    return register.metrics();
  }
}

module.exports = new Metrics();



