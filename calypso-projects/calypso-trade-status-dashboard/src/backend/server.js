const express = require('express');
const cors = require('cors');
const http = require('http');
const WebSocket = require('ws');
const config = require('../config/config');
const logger = require('../utils/logger');
const calypsoClient = require('../services/calypsoClient');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server: config.server.wsPort });

app.use(cors());
app.use(express.json());

// WebSocket connection handling
const clients = new Set();

wss.on('connection', (ws) => {
  logger.info('New WebSocket client connected');
  clients.add(ws);

  ws.on('close', () => {
    logger.info('WebSocket client disconnected');
    clients.delete(ws);
  });

  // Send initial data
  broadcastTrades();
});

function broadcastTrades(filters = {}) {
  calypsoClient.getTrades(filters)
    .then(trades => {
      const message = JSON.stringify({ type: 'trades', data: trades });
      clients.forEach(client => {
        if (client.readyState === WebSocket.OPEN) {
          client.send(message);
        }
      });
    })
    .catch(error => {
      logger.error('Error broadcasting trades', error);
    });
}

// REST API endpoints
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.get('/api/trades', async (req, res) => {
  try {
    const filters = {
      book: req.query.book,
      counterparty: req.query.counterparty,
      status: req.query.status,
      startDate: req.query.startDate,
      endDate: req.query.endDate
    };

    const trades = await calypsoClient.getTrades(filters);
    res.json(trades);
  } catch (error) {
    logger.error('Error fetching trades', error);
    res.status(500).json({ error: 'Failed to fetch trades' });
  }
});

app.get('/api/trades/:id', async (req, res) => {
  try {
    const trade = await calypsoClient.getTradeById(req.params.id);
    if (trade) {
      res.json(trade);
    } else {
      res.status(404).json({ error: 'Trade not found' });
    }
  } catch (error) {
    logger.error('Error fetching trade', error);
    res.status(500).json({ error: 'Failed to fetch trade' });
  }
});

app.post('/api/trades/refresh', (req, res) => {
  const filters = req.body.filters || {};
  broadcastTrades(filters);
  res.json({ message: 'Refresh triggered' });
});

// Polling interval for real-time updates
setInterval(() => {
  if (clients.size > 0) {
    broadcastTrades();
  }
}, 5000); // Update every 5 seconds

// Initialize Calypso client
calypsoClient.authenticate()
  .then(() => {
    server.listen(config.server.port, () => {
      logger.info(`Server running on port ${config.server.port}`);
      logger.info(`WebSocket server running on port ${config.server.wsPort}`);
    });
  })
  .catch(error => {
    logger.error('Failed to initialize Calypso client', error);
    process.exit(1);
  });

module.exports = { app, server, wss };



