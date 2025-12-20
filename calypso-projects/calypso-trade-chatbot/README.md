# Calypso Trade Query Chatbot

AI-powered trade query chatbot that translates natural language queries to Calypso API calls.

## Features

- 💬 Natural language query interface
- 🔄 Translate queries to Calypso API calls
- 📊 Support complex queries (exposure, risk, trades)
- 🧠 Context-aware responses
- 📝 Query history

## Installation

```bash
npm install
```

## Usage

```bash
node src/index.js
```

API endpoint: http://localhost:3000/api/chat

Example query:
```bash
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is our total exposure to Deutsche Bank for December 2025?"}'
```

## Configuration

Create a `.env` file:

```env
CALYPSO_API_BASE_URL=https://calypso-api.example.com
CALYPSO_API_KEY=your_api_key
OPENAI_API_KEY=your_openai_key
MOCK_MODE=true
PORT=3000
```

## License

MIT



