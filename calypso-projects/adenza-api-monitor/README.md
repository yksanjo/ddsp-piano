# Adenza API Performance Monitor

> **Enterprise API Monitoring for Nasdaq IT Operations**

Production-grade API performance monitoring solution designed for Adenza Capital Markets platform, ensuring Nasdaq's REST services meet SLA requirements with comprehensive metrics, real-time alerting, and operational dashboards.

## 🎯 Built for Nasdaq IT Operations

Nasdaq's trading operations depend on Adenza API performance. This monitor provides IT operations teams with real-time visibility into API health, enabling proactive issue detection and ensuring services meet performance SLAs.

## ✨ Key Features

- **📊 Continuous Monitoring**: Automated pinging of Adenza REST endpoints
- **⏱️ Latency Tracking**: Measure and track response times
- **🚨 Intelligent Alerting**: Configurable alerts for performance degradation
- **📈 Historical Metrics**: Prometheus metrics for trend analysis
- **📊 Operational Dashboard**: Real-time dashboard for IT teams
- **🔍 Endpoint Health**: Individual endpoint status and performance

## 💼 Business Value for Nasdaq

### SLA Compliance
- **Performance Assurance**: Ensure APIs meet 200ms response time SLA
- **Proactive Monitoring**: Detect issues before they impact users
- **SLA Reporting**: Metrics for SLA compliance reporting

### Operational Excellence
- **Early Detection**: Identify performance degradation immediately
- **Capacity Planning**: Historical data supports infrastructure planning
- **Incident Prevention**: Prevent outages through proactive monitoring

### Integration
- **Prometheus Compatible**: Integrates with existing monitoring infrastructure
- **Alert Integration**: Connect to Nasdaq's alerting systems
- **Dashboard Integration**: Embed in existing operational dashboards

### Cost Optimization
- **Resource Optimization**: Identify underperforming endpoints for optimization
- **Infrastructure Planning**: Data-driven capacity planning
- **Efficiency Gains**: Automated monitoring reduces manual effort

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

# Monitoring Configuration
MONITOR_INTERVAL=60000  # Check every 60 seconds
PORT=3000

# Alert Thresholds (milliseconds)
PRICE_DISCOVERY_THRESHOLD=200
TRADE_STATUS_THRESHOLD=200
RISK_DATA_THRESHOLD=300

# Alerting (Optional)
EMAIL_ALERTS_ENABLED=false
SLACK_ALERTS_ENABLED=true
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### Running the Monitor

```bash
node src/index.js
```

**Access Points:**
- Dashboard: `http://localhost:3000/dashboard`
- Prometheus Metrics: `http://localhost:3000/metrics`
- Health Check: `http://localhost:3000/health`

## 📊 Monitoring Capabilities

### Endpoint Monitoring
- **Price Discovery API**: Monitor pricing service performance
- **Trade Status API**: Track trade query performance
- **Risk Data API**: Monitor risk calculation performance
- **Custom Endpoints**: Add any Adenza API endpoint

### Metrics Collected
- **Response Time**: Latency in milliseconds
- **Status Codes**: HTTP status code tracking
- **Error Rates**: Failed request tracking
- **Availability**: Uptime percentage

### Prometheus Metrics
- `adenza_api_latency_seconds`: Response time histogram
- `adenza_api_requests_total`: Request counter by status
- `adenza_api_errors_total`: Error counter

## 🚨 Alerting

### Alert Conditions
- Response time exceeds threshold (default: 200ms)
- Endpoint returns error status
- Endpoint becomes unavailable

### Alert Channels
- **Slack**: Real-time notifications to operations channels
- **Email**: Email alerts for critical issues
- **Custom**: Extensible for other notification systems

## 📈 Dashboard Features

- **Real-Time Status**: Current status of all monitored endpoints
- **Performance Trends**: Historical performance graphs
- **Alert History**: Recent alerts and resolutions
- **Endpoint Details**: Individual endpoint performance metrics

## 🔍 Use Cases

1. **SLA Monitoring**: Ensure APIs meet performance SLAs
2. **Capacity Planning**: Use historical data for infrastructure planning
3. **Incident Response**: Quick identification of performance issues
4. **Performance Optimization**: Identify endpoints needing optimization
5. **Regulatory Reporting**: Metrics for regulatory compliance

## 🔧 Customization

- **Custom Endpoints**: Add monitoring for additional Adenza APIs
- **Threshold Configuration**: Set custom thresholds per endpoint
- **Alert Rules**: Configure custom alerting logic
- **Dashboard Customization**: Modify dashboard for specific needs

## 📝 License

MIT License - See LICENSE file for details

---

**Built for Adenza Capital Markets Platform | Optimized for Nasdaq IT Operations**
