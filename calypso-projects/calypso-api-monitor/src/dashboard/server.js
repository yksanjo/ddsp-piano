const express = require('express');
const monitor = require('../monitor');
const metrics = require('../metrics/prometheus');
const alertManager = require('../alerts/alertManager');
const config = require('../config/config');

const app = express();

// Prometheus metrics endpoint
app.get('/metrics', async (req, res) => {
  try {
    const metricsData = await metrics.getMetrics();
    res.set('Content-Type', 'text/plain');
    res.send(metricsData);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Health endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Dashboard endpoint
app.get('/dashboard', (req, res) => {
  res.json({
    endpoints: monitor.endpoints.map(e => e.name),
    alerts: alertManager.getAlertHistory().slice(-10),
    status: 'running'
  });
});

// Start server
const port = config.server.port || 3000;
app.listen(port, () => {
  console.log(`API Monitor dashboard running on port ${port}`);
  console.log(`Metrics available at http://localhost:${port}/metrics`);
  console.log(`Dashboard available at http://localhost:${port}/dashboard`);
});

module.exports = app;



