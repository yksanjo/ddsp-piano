# SAP Transaction Code Finder 🔍

> **Find SAP transaction codes instantly** - Search thousands of SAP transaction codes by description, module, or natural language. The fastest way to discover SAP transactions.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**SAP Transaction Code Finder** helps you find the right SAP transaction code quickly. Instead of searching through documentation or asking colleagues, simply search by what you want to do.

## 🎯 Features

- 🔍 **Smart Search** - Search by description, keywords, or natural language
- 📚 **Comprehensive Database** - 5,000+ SAP transaction codes
- 🏷️ **Module Filtering** - Filter by SAP module (FI, CO, SD, MM, HR, etc.)
- 📊 **Usage Statistics** - See how often transactions are used
- 💡 **Suggestions** - Get similar transaction recommendations
- 🌐 **Web Interface** - Beautiful, modern search interface
- 📱 **CLI Tool** - Command-line interface for power users
- 🔗 **Documentation Links** - Direct links to SAP documentation

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yksanjo/sap-transaction-finder.git
cd sap-transaction-finder

# Install dependencies
pip install -r requirements.txt

# Run the web interface
python app.py
```

## 🚀 Quick Start

### Web Interface

```bash
python app.py
# Open http://localhost:5000
```

### Command Line

```bash
# Search for transactions
python finder.py "invoice"

# Filter by module
python finder.py "purchase order" --module MM

# Get transaction details
python finder.py --code ME23N
```

### Python API

```python
from sap_transaction_finder import TransactionFinder

finder = TransactionFinder()

# Search
results = finder.search("unpaid invoices")
print(results)

# Get transaction details
tx = finder.get_transaction("FBL1N")
print(tx.description, tx.module)
```

## 📚 Example Searches

```
"show invoices" → FBL1N, FBL3N, FB03
"create purchase order" → ME21N, ME21
"view sales order" → VA03, VA05
"material stock" → MMBE, MB52
"customer master" → XD03, VD03
```

## 🎨 Features

### Search Modes
- **Keyword Search** - Fast exact matches
- **Fuzzy Search** - Find even with typos
- **Natural Language** - "Show me invoices" finds FBL1N
- **Module Filter** - Narrow by FI, CO, SD, MM, etc.

### Transaction Details
- Full description
- SAP module
- Transaction type (display/create/change)
- Related transactions
- Documentation links
- Usage frequency

## 📊 Database

Includes transaction codes for:
- **FI** (Financial Accounting)
- **CO** (Controlling)
- **SD** (Sales & Distribution)
- **MM** (Materials Management)
- **HR** (Human Resources)
- **PP** (Production Planning)
- **PM** (Plant Maintenance)
- **BASIS** (System Administration)

## 🤝 Contributing

We welcome contributions! Add more transaction codes, improve search, or enhance the UI.

## 📄 License

MIT License

---

**Find SAP transactions faster. Work smarter, not harder.** 🚀

