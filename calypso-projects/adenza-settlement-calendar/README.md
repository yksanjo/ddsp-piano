# Adenza Settlement Calendar

> **Settlement Holiday Management for Nasdaq Trading Operations**

Interactive settlement calendar application designed for Adenza Capital Markets platform, helping Nasdaq trading teams visualize currency-specific holidays, plan settlement dates, and avoid liquidity gaps that could impact trading operations.

## 🎯 Built for Nasdaq Trading Planning

Settlement holidays vary by currency and can create liquidity gaps if not properly planned. This calendar integrates with Adenza's Holiday Service API to provide Nasdaq traders with a clear view of settlement blackout dates, enabling proactive trade planning and liquidity management.

## ✨ Key Features

- **📅 Interactive Calendar**: FullCalendar-powered visualization of settlement holidays
- **🌍 Multi-Currency Support**: View holidays for any currency pair (USD/JPY, EUR/USD, etc.)
- **🚫 Blackout Highlighting**: Clearly marked settlement holidays
- **🔍 Currency Pair Filtering**: Filter by specific currency pairs
- **📥 iCal Export**: Export calendar to Outlook, Google Calendar, and other systems
- **🔄 Real-Time Updates**: Connect to Adenza Holiday Service API for live data

## 💼 Business Value for Nasdaq

### Liquidity Management
- **Avoid Liquidity Gaps**: Plan trades to avoid settlement on holidays
- **Proactive Planning**: Identify blackout dates well in advance
- **Multi-Currency Awareness**: Manage holidays across all traded currency pairs

### Operational Excellence
- **Trade Planning**: Schedule trades around settlement calendars
- **Settlement Optimization**: Optimize settlement dates for liquidity
- **Risk Reduction**: Prevent failed settlements due to holiday confusion

### Integration
- **Calendar Integration**: Export to standard calendar applications
- **Team Coordination**: Share settlement calendars across Nasdaq teams
- **Automated Updates**: Sync with Adenza Holiday Service for accuracy

### User Experience
- **Visual Clarity**: Intuitive calendar interface
- **Easy Filtering**: Quick access to relevant currency pairs
- **Export Options**: Integration with existing calendar tools

## 🚀 Quick Start

### Installation

```bash
npm install
```

### Configuration

Create a `.env` file:

```env
# Adenza API Configuration
ADENZA_API_BASE_URL=https://your-adenza-instance.com/api
ADENZA_API_KEY=your_api_key_here

# Development Mode
MOCK_MODE=false
```

### Running the Application

```bash
npm start
```

The calendar will open at `http://localhost:3000`

## 📅 Calendar Features

### View Modes
- **Month View**: Overview of all holidays in the month
- **Week View**: Detailed weekly settlement schedule
- **Day View**: Focus on specific dates

### Currency Pair Selection
- Select from common pairs: USD/JPY, EUR/USD, GBP/USD, etc.
- Custom currency pair support
- Multi-pair comparison

### Holiday Information
- Holiday name and description
- Currency-specific holidays
- Settlement impact information

## 📥 Export Options

### iCal Format
- Standard calendar format
- Compatible with Outlook, Google Calendar, Apple Calendar
- Includes all holidays for selected currency pairs

### Integration
- Subscribe to calendar feed
- Automatic updates when holidays change
- Team-wide calendar sharing

## 🔍 Use Cases

1. **Trade Planning**: Plan trade execution dates around settlement holidays
2. **Liquidity Management**: Identify periods with reduced liquidity
3. **Settlement Scheduling**: Optimize settlement dates for cash management
4. **Team Coordination**: Share settlement calendars across trading desks
5. **Regulatory Compliance**: Ensure trades don't settle on invalid dates

## 🎨 Customization

- **Custom Currency Pairs**: Add support for additional currency pairs
- **Holiday Rules**: Configure custom settlement rules
- **Visual Styling**: Customize calendar appearance
- **Notifications**: Add alerts for upcoming holidays

## 🔧 Technical Architecture

- **Frontend**: React.js with FullCalendar integration
- **API Integration**: Adenza Holiday Service API
- **Export**: iCal generator for calendar export
- **Date Calculations**: Settlement date calculation utilities

## 📝 License

MIT License - See LICENSE file for details

---

**Built for Adenza Capital Markets Platform | Optimized for Nasdaq Trading Planning**
