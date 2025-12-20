# Adenza Static Data Health Check

> **Data Quality Assurance for Nasdaq Regulatory Compliance**

Enterprise-grade static data validation tool designed for Adenza Capital Markets platform, ensuring Nasdaq's Legal Entities, Books, and Portfolios meet regulatory requirements and data quality standards before trades are entered.

## 🎯 Built for Nasdaq Data Governance

Regulatory compliance requires accurate, complete static data. This tool proactively validates Adenza static data against industry standards (LEI codes, ISO currency codes, etc.), preventing trades from being entered with incomplete or invalid data that could cause settlement failures or regulatory issues.

## ✨ Key Features

- **🔍 Comprehensive Scanning**: Validates Legal Entities, Books, and Portfolios
- **✅ Regulatory Compliance**: Checks for required fields (LEI codes, country codes, etc.)
- **📊 Health Scoring**: Automated data quality score (0-100%)
- **📈 Detailed Reporting**: Comprehensive reports with specific issues identified
- **🚨 Issue Detection**: Identifies orphaned records and incomplete entries
- **🔄 Automated Validation**: Batch validation of entire static data set

## 💼 Business Value for Nasdaq

### Regulatory Compliance
- **LEI Validation**: Ensures Legal Entity Identifiers are present and valid
- **ISO Standards**: Validates currency codes, country codes against ISO standards
- **Audit Readiness**: Automated reports support regulatory audits
- **Compliance Confidence**: Proactive validation prevents compliance issues

### Data Quality
- **Early Detection**: Identify data issues before they impact trading
- **Completeness**: Ensure all required fields are populated
- **Consistency**: Validate data consistency across entities
- **Accuracy**: Verify data format and validity

### Risk Reduction
- **Settlement Prevention**: Prevent trades with incomplete static data
- **Operational Risk**: Reduce operational errors from bad data
- **Reputation Risk**: Avoid regulatory penalties from data issues

### Operational Efficiency
- **Automated Validation**: Eliminate manual data quality checks
- **Bulk Processing**: Validate entire static data set efficiently
- **Prioritized Issues**: Focus on critical data quality issues first

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

# Development Mode
MOCK_MODE=false
```

### Usage

**Run Health Check:**
```bash
node src/index.js
```

**Output:**
- Console summary with health score and issue counts
- Detailed report saved to `health-check-report-{timestamp}.txt`

## 📊 Validation Rules

### Legal Entities
- ✅ LEI (Legal Entity Identifier) present and valid format
- ✅ Legal name present
- ✅ Country code present and valid
- ✅ Required regulatory fields populated

### Books
- ✅ Book ID or name present
- ✅ Legal entity reference valid
- ✅ Base currency present and valid ISO 4217 code
- ✅ Book type specified

### Portfolios
- ✅ Portfolio ID or name present
- ✅ Book reference valid
- ✅ Portfolio type specified
- ✅ Required relationships maintained

## 📈 Health Score Calculation

Health Score = (Valid Records / Total Records) × 100

- **90-100%**: Excellent data quality
- **75-89%**: Good, minor issues to address
- **50-74%**: Fair, significant issues require attention
- **<50%**: Poor, critical data quality issues

## 📊 Report Format

The tool generates comprehensive reports including:

1. **Executive Summary**
   - Overall health score
   - Total records scanned
   - Issue counts by type

2. **Detailed Issues**
   - Specific records with issues
   - Field-level problems identified
   - Recommended actions

3. **Statistics**
   - Breakdown by entity type
   - Issue distribution
   - Trend analysis (if run regularly)

## 🔍 Use Cases

1. **Pre-Trading Validation**: Run before major trading activities
2. **Regular Audits**: Scheduled data quality checks
3. **Post-Migration**: Validate data after system migrations
4. **Regulatory Preparation**: Ensure compliance before regulatory submissions
5. **Data Cleanup Projects**: Identify records requiring attention

## 🔧 Customization

- **Custom Validators**: Add validation rules for specific business requirements
- **Integration**: Integrate with Nasdaq's data quality tools
- **Automation**: Schedule regular health checks via cron or CI/CD
- **Notifications**: Add alerts for critical data quality issues

## 📝 License

MIT License - See LICENSE file for details

---

**Built for Adenza Capital Markets Platform | Optimized for Nasdaq Data Governance**
