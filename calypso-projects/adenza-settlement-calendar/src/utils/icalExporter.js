const ical = require('ical-generator');
const { saveAs } = require('file-saver');

class ICalExporter {
  export(events, filename = 'settlement-calendar.ics') {
    const calendar = ical({
      prodId: {
        company: 'Adenza',
        product: 'Settlement Calendar',
        language: 'EN'
      },
      name: 'Settlement Calendar',
      timezone: 'UTC'
    });

    events.forEach(event => {
      calendar.createEvent({
        start: new Date(event.start),
        end: new Date(event.start),
        summary: event.title,
        allDay: true
      });
    });

    const icalString = calendar.toString();
    const blob = new Blob([icalString], { type: 'text/calendar;charset=utf-8' });
    saveAs(blob, filename);
  }
}

module.exports = new ICalExporter();

