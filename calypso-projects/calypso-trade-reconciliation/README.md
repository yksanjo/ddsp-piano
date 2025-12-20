# Calypso Trade Reconciliation Tool

Automated trade reconciliation tool that compares Calypso trades with external CSV or SWIFT files.

## Features

- 📄 Parse CSV and SWIFT files
- 🔍 Compare trades and highlight discrepancies
- 📊 Generate reconciliation reports
- 📧 Email notifications for mismatches

## Installation

```bash
npm install
```

## Usage

```bash
node src/index.js <external-file> [file-type]
```

Example:
```bash
node src/index.js trades.csv csv
node src/index.js trades.txt swift
```

## Configuration

Create a `.env` file:

```env
CALYPSO_API_BASE_URL=https://calypso-api.example.com
CALYPSO_API_KEY=your_api_key
MOCK_MODE=true
EMAIL_ENABLED=false
```

## License

MIT



