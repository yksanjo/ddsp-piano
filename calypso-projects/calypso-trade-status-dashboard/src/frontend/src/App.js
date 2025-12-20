import React, { useState, useEffect } from 'react';
import axios from 'axios';
import TradeStatusCard from './components/TradeStatusCard';
import TradeFilters from './components/TradeFilters';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001';
const WS_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:3002';

function App() {
  const [trades, setTrades] = useState([]);
  const [filters, setFilters] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTrades();
    connectWebSocket();
  }, []);

  useEffect(() => {
    fetchTrades();
  }, [filters]);

  const fetchTrades = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      Object.keys(filters).forEach(key => {
        if (filters[key]) {
          params.append(key, filters[key]);
        }
      });

      const response = await axios.get(`${API_BASE_URL}/api/trades?${params}`);
      setTrades(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch trades. Please check your connection.');
      console.error('Error fetching trades:', err);
    } finally {
      setLoading(false);
    }
  };

  const connectWebSocket = () => {
    const ws = new WebSocket(WS_URL);

    ws.onopen = () => {
      console.log('WebSocket connected');
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      if (message.type === 'trades') {
        setTrades(message.data);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected. Reconnecting...');
      setTimeout(connectWebSocket, 3000);
    };
  };

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
  };

  const handleExportCSV = () => {
    const csvContent = [
      ['Trade ID', 'Trade Date', 'Book', 'Counterparty', 'Instrument', 'Notional', 'Status', 'Last Update'],
      ...trades.map(trade => [
        trade.id,
        trade.tradeDate,
        trade.book,
        trade.counterparty,
        trade.instrument,
        trade.notional,
        trade.status,
        trade.lastUpdate
      ])
    ].map(row => row.join(',')).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `trades_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const statusCounts = trades.reduce((acc, trade) => {
    acc[trade.status] = (acc[trade.status] || 0) + 1;
    return acc;
  }, {});

  return (
    <div className="App">
      <header className="App-header">
        <h1>Calypso Trade Status Dashboard</h1>
        <div className="status-summary">
          <div className="status-item pending">
            <span className="status-label">Pending:</span>
            <span className="status-count">{statusCounts.Pending || 0}</span>
          </div>
          <div className="status-item confirmed">
            <span className="status-label">Confirmed:</span>
            <span className="status-count">{statusCounts.Confirmed || 0}</span>
          </div>
          <div className="status-item settled">
            <span className="status-label">Settled:</span>
            <span className="status-count">{statusCounts.Settled || 0}</span>
          </div>
        </div>
      </header>

      <main className="App-main">
        <TradeFilters onFilterChange={handleFilterChange} />
        
        <div className="actions">
          <button onClick={fetchTrades} disabled={loading}>
            {loading ? 'Loading...' : 'Refresh'}
          </button>
          <button onClick={handleExportCSV} disabled={trades.length === 0}>
            Export CSV
          </button>
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="trades-grid">
          {trades.map(trade => (
            <TradeStatusCard key={trade.id} trade={trade} />
          ))}
        </div>

        {trades.length === 0 && !loading && (
          <div className="no-trades">No trades found matching the filters.</div>
        )}
      </main>
    </div>
  );
}

export default App;



