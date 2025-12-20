# Adenza SWIFT Simulator

> **SWIFT Message Generation for Nasdaq Back-Office Testing**

Enterprise SWIFT message simulator designed for Adenza Capital Markets platform, enabling Nasdaq back-office teams to test settlement workflows and message processing without requiring live SWIFT network connections or expensive test environment subscriptions.

## 🎯 Built for Nasdaq Back-Office Operations

Testing settlement workflows requires SWIFT messages, but accessing the SWIFT network for testing is costly and complex. This simulator generates realistic SWIFT messages (MT103, MT300, etc.) from Adenza trade data, enabling comprehensive testing without SWIFT network dependencies.

## ✨ Key Features

- **📨 Multiple Message Types**: Generate MT103 (Payment), MT300 (FX Confirmation), and more
- **✅ Format Validation**: Built-in SWIFT message format validation
- **🔄 Trade Integration**: Generate messages from Adenza trade data
- **💾 Export Options**: Save to file or send via API
- **🔧 Template-Based**: Flexible template system for custom message types
- **📊 Batch Generation**: Generate multiple messages from trade lists

## 💼 Business Value for Nasdaq

### Testing Efficiency
- **No SWIFT Network Required**: Test settlement workflows without SWIFT access
- **Instant Generation**: Create test messages in seconds vs. hours
- **Realistic Data**: Messages based on actual Adenza trade data

### Cost Reduction
- **Eliminate Test Environment Costs**: No need for SWIFT test environment subscriptions
- **Reduce Testing Time**: Faster test cycles with instant message generation
- **Lower Infrastructure Costs**: Test without dedicated SWIFT infrastructure

### Development Speed
- **Faster Development**: Developers can test immediately without waiting for SWIFT setup
- **Parallel Testing**: Multiple teams can test simultaneously
- **CI/CD Integration**: Automated message generation in test pipelines

### Quality Assurance
- **Format Validation**: Ensure messages meet SWIFT standards before production
- **Comprehensive Testing**: Test all message types and scenarios
- **Regression Testing**: Generate consistent test messages for regression tests

## 🚀 Quick Start

### Installation

```bash
npm install
```

### Configuration

Create a `.env` file:

```env
# Adenza API Configuration (for fetching trade data)
ADENZA_API_BASE_URL=https://your-adenza-instance.com/api
ADENZA_API_KEY=your_api_key_here

# Development Mode
MOCK_MODE=false
```

### Usage

**Generate MT103 from Trade ID:**
```bash
node src/index.js MT103 TRD-001 output.swift
```

**Generate MT300 (FX Confirmation):**
```bash
node src/index.js MT300 TRD-002 fx-confirmation.swift
```

**Generate with Mock Data:**
```bash
node src/index.js MT103
# Uses mock trade data if no trade ID provided
```

## 📨 Supported Message Types

### MT103 - Customer Credit Transfer
- Payment messages for trade settlements
- Includes amount, currency, counterparty details
- Validates required SWIFT fields

### MT300 - Foreign Exchange Confirmation
- FX trade confirmations
- Includes currency pairs, rates, amounts
- Settlement date information

### Extensible Architecture
- Easy to add new message types
- Template-based generation
- Custom field support

## 🔍 Message Validation

The simulator validates generated messages for:
- ✅ Required SWIFT blocks (1, 2, 4, 5)
- ✅ Field presence and format
- ✅ Balanced braces
- ✅ Message type-specific requirements

## 📊 Use Cases

1. **Settlement Testing**: Test settlement workflows with realistic SWIFT messages
2. **Message Processing**: Validate SWIFT message parsing logic
3. **Integration Testing**: Test integration with SWIFT processing systems
4. **Training**: Generate sample messages for team training
5. **Development**: Create test data for development environments

## 🔧 Customization

### Adding New Message Types

Create new templates in `src/templates/`:

```javascript
class MTXXXTemplate {
  generate(tradeData) {
    // Generate SWIFT message
    return message;
  }
}
```

### Custom Validation

Extend `src/validators/swiftValidator.js` for custom validation rules.

## 📝 License

MIT License - See LICENSE file for details

---

**Built for Adenza Capital Markets Platform | Optimized for Nasdaq Back-Office Testing**
