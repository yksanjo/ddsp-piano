import React from 'react';
import './TradeStatusCard.css';

const TradeStatusCard = ({ trade }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'Pending':
        return '#ffa500';
      case 'Confirmed':
        return '#00ff00';
      case 'Settled':
        return '#008000';
      default:
        return '#ccc';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'Pending':
        return '⏳';
      case 'Confirmed':
        return '✓';
      case 'Settled':
        return '✓✓';
      default:
        return '?';
    }
  };

  return (
    <div className="trade-card" style={{ borderLeftColor: getStatusColor(trade.status) }}>
      <div className="trade-header">
        <div className="trade-id">{trade.id}</div>
        <div className="trade-status" style={{ backgroundColor: getStatusColor(trade.status) }}>
          {getStatusIcon(trade.status)} {trade.status}
        </div>
      </div>
      
      <div className="trade-details">
        <div className="detail-row">
          <span className="detail-label">Instrument:</span>
          <span className="detail-value">{trade.instrument}</span>
        </div>
        <div className="detail-row">
          <span className="detail-label">Book:</span>
          <span className="detail-value">{trade.book}</span>
        </div>
        <div className="detail-row">
          <span className="detail-label">Counterparty:</span>
          <span className="detail-value">{trade.counterparty}</span>
        </div>
        <div className="detail-row">
          <span className="detail-label">Notional:</span>
          <span className="detail-value">{trade.notional.toLocaleString()}</span>
        </div>
        <div className="detail-row">
          <span className="detail-label">Trade Date:</span>
          <span className="detail-value">{trade.tradeDate}</span>
        </div>
        <div className="detail-row">
          <span className="detail-label">Last Update:</span>
          <span className="detail-value">{new Date(trade.lastUpdate).toLocaleString()}</span>
        </div>
      </div>
    </div>
  );
};

export default TradeStatusCard;



