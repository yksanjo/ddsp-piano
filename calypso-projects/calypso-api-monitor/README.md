# Calypso API Performance Monitor

API performance monitor that pings Calypso REST endpoints and alerts on latency issues.

## Features

- 📊 Ping Calypso REST endpoints
- ⏱️ Measure latency and response times
- 🚨 Alert if response time > 200ms
- 📈 Historical performance tracking
- 📊 Prometheus metrics

## Installation

```bash
npm install
```

## Usage

```bash
node src/index.js
```

Access dashboard at: http://localhost:3000/dashboard
Metrics at: http://localhost:3000/metrics

## Configuration

Create a `.env` file:

```env
CALYPSO_API_BASE_URL=https://calypso-api.example.com
CALYPSO_API_KEY=your_api_key
MONITOR_INTERVAL=60000
PORT=3000
```

## License

MIT



