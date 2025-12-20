#!/usr/bin/env node

const monitor = require('./monitor');
const dashboard = require('./dashboard/server');
const config = require('./config/config');
const logger = require('./utils/logger');

async function main() {
  try {
    logger.info('Starting Calypso API Monitor...');

    // Start monitoring
    const intervalMs = config.monitor.interval || 60000; // 1 minute default
    monitor.start(intervalMs);

    // Start dashboard (already starts server in dashboard/server.js)
    // dashboard is imported to start the Express server

    logger.info('API Monitor started successfully');

    // Graceful shutdown
    process.on('SIGINT', () => {
      logger.info('Shutting down...');
      monitor.stop();
      process.exit(0);
    });
  } catch (error) {
    logger.error('Failed to start monitor', error);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { main };



