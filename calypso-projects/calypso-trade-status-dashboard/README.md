# Calypso Trade Status Dashboard

Real-time trade status dashboard for Calypso trading platform with traffic light visualization and WebSocket support.

## Features

- 🚦 Traffic light visualization (Pending/Confirmed/Settled)
- 🔄 Real-time updates via WebSocket or polling
- 🔍 Filter by book, counterparty, date range
- 📊 Export to CSV
- ⚠️ Alert system for stuck trades

## Installation

```bash
npm install
cd src/frontend && npm install
```

## Configuration

Create a `.env` file:

```env
CALYPSO_API_BASE_URL=https://calypso-api.example.com
CALYPSO_API_KEY=your_api_key
CALYPSO_API_SECRET=your_api_secret
PORT=3001
WS_PORT=3002
MOCK_MODE=true
```

## Usage

### Development

```bash
npm run dev
```

### Production

```bash
npm run build
npm start
```

## Tech Stack

- React.js (Frontend)
- Express.js (Backend)
- WebSocket (Real-time updates)
- Calypso REST API

## License

MIT



