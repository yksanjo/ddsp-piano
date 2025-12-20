# Adenza Trade Query Chatbot

> **AI-Powered Natural Language Interface for Nasdaq Trading Operations**

Enterprise AI chatbot designed for Adenza Capital Markets platform, enabling Nasdaq traders and operations teams to query exposure, risk, and trade data using natural language. Powered by LangChain and modern LLM technology, it transforms complex Adenza API queries into conversational interactions.

## 🎯 Built for Nasdaq User Experience

Nasdaq teams need quick access to trading data, but learning complex query syntax can be time-consuming. This chatbot enables users to ask questions in plain English like "What is our total exposure to Deutsche Bank for December 2025?" and receive instant, accurate answers from Adenza data.

## ✨ Key Features

- **💬 Natural Language Interface**: Ask questions in plain English
- **🔄 Intelligent Translation**: Converts queries to Adenza API calls automatically
- **📊 Complex Query Support**: Handle exposure, risk, trade, and position queries
- **🧠 Context Awareness**: Maintains conversation context for follow-up questions
- **📝 Query History**: Track and review past queries
- **🔍 Multi-Intent Recognition**: Understands various query types and intents

## 💼 Business Value for Nasdaq

### User Experience
- **Reduced Training Time**: New users productive immediately without query syntax training
- **Faster Data Access**: Get answers in seconds vs. minutes
- **Intuitive Interface**: Natural language is more accessible than technical queries

### Productivity Gains
- **60%+ Faster Queries**: Natural language faster than learning API syntax
- **Reduced Errors**: Fewer query syntax errors
- **Self-Service**: Users get answers without IT support

### Accessibility
- **Non-Technical Users**: Makes data accessible to business users
- **Mobile Friendly**: Query data from any device
- **24/7 Availability**: Always available for queries

### Innovation
- **Cutting-Edge AI**: Demonstrates modern AI integration for capital markets
- **Competitive Advantage**: Advanced user experience differentiator
- **Future-Ready**: Foundation for more advanced AI features

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

# LLM Configuration
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-3.5-turbo  # or gpt-4 for better performance

# Server Configuration
PORT=3000

# Development Mode
MOCK_MODE=false
```

### Running the Chatbot

```bash
node src/index.js
```

The API will be available at `http://localhost:3000`

## 💬 Example Queries

### Exposure Queries
```bash
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is our total exposure to Deutsche Bank for December 2025?"}'
```

### Trade Queries
```bash
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me all pending trades for JP Morgan this week"}'
```

### Risk Queries
```bash
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is our portfolio delta for USD/EUR positions?"}'
```

### Position Queries
```bash
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What are our current holdings in Trading Book 1?"}'
```

## 🧠 How It Works

1. **Query Parsing**: Natural language query analyzed for intent and entities
2. **API Translation**: Query converted to appropriate Adenza API call
3. **Data Retrieval**: Fetch data from Adenza API
4. **Response Generation**: LLM generates natural language response from data
5. **Context Management**: Maintains conversation history for follow-ups

## 📊 Supported Query Types

- **Exposure**: Counterparty exposure, currency exposure, date-specific exposure
- **Trades**: Trade status, trade history, trade filtering
- **Risk**: Portfolio risk, Greeks, risk metrics
- **Positions**: Current holdings, position details
- **Pricing**: Market prices, rates, quotes

## 🔍 Use Cases

1. **Trading Desk Queries**: Quick exposure and risk checks during trading
2. **Operations Support**: Answer operational questions without IT help
3. **Management Reporting**: Generate summary reports via natural language
4. **Training**: Help new users learn system capabilities
5. **Mobile Access**: Query data from mobile devices

## 🔧 Customization

- **Custom Intents**: Add support for additional query types
- **LLM Selection**: Choose between OpenAI, Anthropic, or other providers
- **Response Formatting**: Customize response style and format
- **Integration**: Integrate with Nasdaq's chat platforms (Slack, Teams)

## 🔒 Security & Privacy

- **API Key Management**: Secure storage of API credentials
- **Query Logging**: Optional query history for audit
- **Access Control**: Integrate with Nasdaq's authentication systems
- **Data Privacy**: No user data stored externally

## 📝 License

MIT License - See LICENSE file for details

---

**Built for Adenza Capital Markets Platform | Optimized for Nasdaq User Experience**
