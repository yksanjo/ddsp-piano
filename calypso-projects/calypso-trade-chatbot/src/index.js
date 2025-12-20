#!/usr/bin/env node

const express = require('express');
const cors = require('cors');
const chatApi = require('./api/chatApi');
const config = require('./config/config');
const logger = require('./utils/logger');

const app = express();

app.use(cors());
app.use(express.json());
app.use('/api', chatApi);

app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

const port = config.server.port || 3000;
app.listen(port, () => {
  logger.info(`Calypso Trade Chatbot API running on port ${port}`);
  console.log(`API available at http://localhost:${port}/api/chat`);
});

module.exports = app;



