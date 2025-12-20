# Calypso Static Data Health Check

Static data health check script that scans Legal Entities, Books, and Portfolios for issues.

## Features

- 🔍 Scan Legal Entities, Books, Portfolios
- ✅ Validate required fields (LEI codes, etc.)
- 📊 Generate health check reports
- 📈 Automated data quality scoring

## Installation

```bash
npm install
```

## Usage

```bash
node src/index.js
```

## Configuration

Create a `.env` file:

```env
CALYPSO_API_BASE_URL=https://calypso-api.example.com
CALYPSO_API_KEY=your_api_key
MOCK_MODE=true
```

## License

MIT



