# Adenza Trade Status Dashboard

> **Enterprise Real-Time Trade Monitoring for Nasdaq Operations**

A production-ready, web-based trade status dashboard designed specifically for Adenza Capital Markets platform, empowering Nasdaq trading and operations teams with instant visibility into trade lifecycles without the overhead of traditional thick-client applications.

## 🎯 Built for Nasdaq's Trading Operations

This dashboard addresses the critical "visibility gap" where Nasdaq teams need real-time insight into trade status across multiple books, counterparties, and instruments. Built on modern web technologies, it seamlessly integrates with Adenza's REST APIs and provides the operational transparency that Nasdaq's high-volume trading environment demands.

## ✨ Key Features

- **🚦 Traffic Light Visualization**: Instant status recognition (Pending/Confirmed/Settled) with color-coded indicators
- **🔄 Real-Time Updates**: WebSocket-powered live updates or configurable polling intervals
- **🔍 Advanced Filtering**: Filter by book, counterparty, instrument, date range, and status
- **📊 CSV Export**: One-click export for reporting and analysis
- **⚠️ Intelligent Alerts**: Automated detection and notification of stuck trades
- **📱 Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

## 💼 Business Value for Nasdaq

### Operational Excellence
- **Eliminate Visibility Gaps**: Middle-office teams can instantly identify where trades are stuck in the settlement pipeline
- **Reduce Manual Effort**: No need to open heavy Adenza client applications for status checks
- **Faster Issue Resolution**: Early detection of problematic trades prevents settlement failures

### Risk Management
- **Proactive Monitoring**: Real-time alerts prevent trades from getting stuck unnoticed
- **Settlement Risk Reduction**: Identify and resolve issues before settlement deadlines
- **Audit Trail**: Complete history of trade status changes for compliance

### Scalability & Integration
- **Modern Architecture**: Built on React.js and Express.js for enterprise-scale performance
- **API-First Design**: Seamlessly integrates with Adenza's REST APIs
- **Nasdaq-Ready**: Designed to handle high-volume trading operations

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm
- Access to Adenza Capital Markets platform APIs (or use mock mode for development)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd adenza-trade-status-dashboard

# Install backend dependencies
npm install

# Install frontend dependencies
cd src/frontend && npm install && cd ../..
```

### Configuration

Create a `.env` file in the root directory:

```env
# Adenza API Configuration
ADENZA_API_BASE_URL=https://your-adenza-instance.com/api
ADENZA_API_KEY=your_api_key_here
ADENZA_API_SECRET=your_api_secret_here

# Server Configuration
PORT=3001
WS_PORT=3002
NODE_ENV=production

# Development Mode (set to true for testing without real API)
MOCK_MODE=false
```

### Running the Application

**Development Mode:**
```bash
npm run dev
```

**Production Mode:**
```bash
npm run build
npm start
```

The dashboard will be available at `http://localhost:3001`

## 🏗️ Architecture

- **Frontend**: React.js with modern hooks and context API
- **Backend**: Express.js REST API server
- **Real-Time**: WebSocket server for live updates
- **API Integration**: Adenza REST API client with OAuth2/API key authentication
- **State Management**: React hooks for efficient state handling

## 📈 Use Cases

1. **Middle-Office Monitoring**: Real-time view of all pending trades across books
2. **Settlement Operations**: Identify trades approaching settlement deadlines
3. **Exception Management**: Quickly locate and resolve stuck trades
4. **Reporting**: Export trade status data for regulatory and internal reporting

## 🔧 Customization

The dashboard is designed for easy customization:
- Modify filters and columns to match your operational needs
- Adjust alert thresholds based on your risk tolerance
- Customize color schemes and branding
- Extend with additional Adenza API endpoints

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

This project is designed to enhance Adenza Capital Markets platform operations. Contributions that improve Nasdaq's trading operations are welcome.

---

**Built for Adenza Capital Markets Platform | Optimized for Nasdaq Trading Operations**
