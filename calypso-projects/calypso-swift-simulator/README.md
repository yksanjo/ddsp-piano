# Calypso SWIFT Simulator

SWIFT message simulator for generating mock SWIFT messages (MT103, MT300, etc.) for testing.

## Features

- 📨 Generate mock SWIFT messages (MT103, MT300, etc.)
- ✅ Validate SWIFT message format
- 💾 Export to file or send via API
- 🔧 Template-based message generation

## Installation

```bash
npm install
```

## Usage

```bash
node src/index.js <message-type> [trade-id] [output-file]
```

Example:
```bash
node src/index.js MT103 TRD-001 output.swift
node src/index.js MT300
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



