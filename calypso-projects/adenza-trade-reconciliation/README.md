# Adenza Trade Reconciliation Tool

> **Automated Trade Reconciliation for Nasdaq Regulatory Compliance**

Enterprise-grade automated reconciliation solution designed for Adenza Capital Markets platform, enabling Nasdaq operations teams to efficiently compare internal trade data with external counterparty files (CSV, SWIFT) to ensure regulatory compliance and operational accuracy.

## 🎯 Purpose-Built for Nasdaq Operations

Reconciliation is a critical operational function for Nasdaq's trading operations. This tool automates the tedious, error-prone process of manually comparing Adenza trade records with counterparty confirmations, reducing operational risk and ensuring regulatory compliance.

## ✨ Key Features

- **📄 Multi-Format Support**: Parse CSV files and SWIFT messages (MT103, MT300, etc.)
- **🔍 Intelligent Comparison**: Advanced diff algorithms identify discrepancies in notional, dates, currencies, and counterparties
- **📊 Comprehensive Reporting**: Detailed reconciliation reports with discrepancy summaries
- **📧 Automated Notifications**: Email alerts for mismatches requiring attention
- **✅ Validation**: Built-in validation for trade data integrity
- **🔄 Batch Processing**: Handle large volumes of trades efficiently

## 💼 Business Value for Nasdaq

### Regulatory Compliance
- **Automated Accuracy**: Ensures trade records match counterparty confirmations for regulatory reporting
- **Audit Trail**: Complete reconciliation history for internal and external audits
- **Compliance Ready**: Meets requirements for trade reconciliation mandates

### Operational Efficiency
- **80%+ Time Savings**: Eliminates manual reconciliation effort
- **Error Reduction**: Automated comparison reduces human error
- **Scalability**: Handles high-volume reconciliation workloads

### Risk Mitigation
- **Early Detection**: Identify discrepancies before settlement
- **Settlement Risk**: Prevent failed settlements due to data mismatches
- **Operational Risk**: Reduce operational losses from reconciliation errors

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

# Email Notifications (Optional)
EMAIL_ENABLED=true
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your_email@example.com
SMTP_PASSWORD=your_password
EMAIL_TO=operations@nasdaq.com
EMAIL_FROM=reconciliation@nasdaq.com

# Development Mode
MOCK_MODE=false
```

### Usage

**Basic Reconciliation:**
```bash
node src/index.js external-trades.csv csv
```

**SWIFT File Reconciliation:**
```bash
node src/index.js swift-messages.txt swift
```

**With Date Range:**
The tool automatically fetches trades from Adenza API and compares with external files.

### Output

The tool generates:
- Console summary of reconciliation results
- Detailed text report saved to `reconciliation-report-{timestamp}.txt`
- Email notification (if enabled) with report attachment

## 📊 Reconciliation Process

1. **Fetch Trades**: Retrieves trades from Adenza API based on date range
2. **Parse External Files**: Processes CSV or SWIFT files from counterparties
3. **Match & Compare**: Matches trades by ID and compares all fields
4. **Identify Discrepancies**: Flags mismatches in:
   - Notional amounts
   - Trade dates
   - Counterparty information
   - Currency codes
   - Instrument details
5. **Generate Report**: Creates comprehensive reconciliation report
6. **Notify**: Sends email alerts for discrepancies (if configured)

## 🔍 Discrepancy Types

- **Missing in External**: Trades in Adenza but not in counterparty file
- **Missing in Adenza**: Trades in counterparty file but not in Adenza
- **Field Mismatch**: Trades exist in both but have different values

## 📈 Use Cases

1. **Daily Reconciliation**: Automated end-of-day reconciliation with counterparties
2. **Regulatory Reporting**: Ensure accuracy for regulatory submissions
3. **Exception Management**: Identify and resolve discrepancies quickly
4. **Audit Support**: Provide reconciliation evidence for audits

## 🔧 Customization

- Extend parsers for additional file formats
- Customize comparison logic for specific business rules
- Integrate with Nasdaq's notification systems
- Add custom validation rules

## 📝 License

MIT License - See LICENSE file for details

---

**Built for Adenza Capital Markets Platform | Optimized for Nasdaq Regulatory Compliance**
