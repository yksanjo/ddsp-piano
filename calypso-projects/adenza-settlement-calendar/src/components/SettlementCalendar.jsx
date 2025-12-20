import React, { useState, useEffect } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import holidayService from '../services/holidayService';
import icalExporter from '../utils/icalExporter';
import './SettlementCalendar.css';

const SettlementCalendar = () => {
  const [events, setEvents] = useState([]);
  const [currencyPair, setCurrencyPair] = useState('USD/JPY');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHolidays();
  }, [currencyPair]);

  const loadHolidays = async () => {
    try {
      setLoading(true);
      const holidays = await holidayService.getHolidays(currencyPair);
      const calendarEvents = holidays.map(holiday => ({
        title: `Holiday: ${holiday.name}`,
        start: holiday.date,
        allDay: true,
        backgroundColor: '#ff6b6b',
        borderColor: '#ff6b6b',
        className: 'holiday-event'
      }));
      setEvents(calendarEvents);
    } catch (error) {
      console.error('Error loading holidays', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = () => {
    icalExporter.export(events, `settlement-calendar-${currencyPair.replace('/', '-')}.ics`);
  };

  const currencyPairs = ['USD/JPY', 'EUR/USD', 'GBP/USD', 'USD/CHF', 'AUD/USD'];

  return (
    <div className="settlement-calendar">
      <div className="calendar-header">
        <h2>Settlement Calendar</h2>
        <div className="controls">
          <label>
            Currency Pair:
            <select value={currencyPair} onChange={(e) => setCurrencyPair(e.target.value)}>
              {currencyPairs.map(pair => (
                <option key={pair} value={pair}>{pair}</option>
              ))}
            </select>
          </label>
          <button onClick={handleExport}>Export iCal</button>
        </div>
      </div>

      {loading ? (
        <div className="loading">Loading holidays...</div>
      ) : (
        <FullCalendar
          plugins={[dayGridPlugin, timeGridPlugin]}
          initialView="dayGridMonth"
          events={events}
          headerToolbar={{
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
          }}
          eventContent={(eventInfo) => (
            <div className="event-content">
              {eventInfo.event.title}
            </div>
          )}
        />
      )}
    </div>
  );
};

export default SettlementCalendar;

