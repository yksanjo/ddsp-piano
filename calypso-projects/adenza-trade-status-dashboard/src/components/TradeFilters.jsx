import React, { useState } from 'react';
import './TradeFilters.css';

const TradeFilters = ({ onFilterChange }) => {
  const [filters, setFilters] = useState({
    book: '',
    counterparty: '',
    status: '',
    startDate: '',
    endDate: ''
  });

  const handleChange = (field, value) => {
    const newFilters = { ...filters, [field]: value };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const handleClear = () => {
    const clearedFilters = {
      book: '',
      counterparty: '',
      status: '',
      startDate: '',
      endDate: ''
    };
    setFilters(clearedFilters);
    onFilterChange(clearedFilters);
  };

  return (
    <div className="trade-filters">
      <h3>Filters</h3>
      <div className="filters-grid">
        <div className="filter-item">
          <label htmlFor="book">Book:</label>
          <input
            id="book"
            type="text"
            value={filters.book}
            onChange={(e) => handleChange('book', e.target.value)}
            placeholder="Filter by book"
          />
        </div>

        <div className="filter-item">
          <label htmlFor="counterparty">Counterparty:</label>
          <input
            id="counterparty"
            type="text"
            value={filters.counterparty}
            onChange={(e) => handleChange('counterparty', e.target.value)}
            placeholder="Filter by counterparty"
          />
        </div>

        <div className="filter-item">
          <label htmlFor="status">Status:</label>
          <select
            id="status"
            value={filters.status}
            onChange={(e) => handleChange('status', e.target.value)}
          >
            <option value="">All Statuses</option>
            <option value="Pending">Pending</option>
            <option value="Confirmed">Confirmed</option>
            <option value="Settled">Settled</option>
          </select>
        </div>

        <div className="filter-item">
          <label htmlFor="startDate">Start Date:</label>
          <input
            id="startDate"
            type="date"
            value={filters.startDate}
            onChange={(e) => handleChange('startDate', e.target.value)}
          />
        </div>

        <div className="filter-item">
          <label htmlFor="endDate">End Date:</label>
          <input
            id="endDate"
            type="date"
            value={filters.endDate}
            onChange={(e) => handleChange('endDate', e.target.value)}
          />
        </div>

        <div className="filter-item">
          <button onClick={handleClear} className="clear-button">
            Clear Filters
          </button>
        </div>
      </div>
    </div>
  );
};

export default TradeFilters;

