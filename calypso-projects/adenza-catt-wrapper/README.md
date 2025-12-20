# Adenza CATT Wrapper

> **Enterprise Test Automation for Adenza Capital Markets Platform**

A production-ready Node.js wrapper for Adenza's CATT (Calypso Automated Testing Tool), designed to integrate automated regression testing into Nasdaq's modern CI/CD pipelines. Enables seamless test execution, result reporting, and team notifications.

## 🎯 Built for Nasdaq DevOps

Nasdaq's development teams need reliable, automated testing integrated into their CI/CD workflows. This wrapper bridges Adenza's CATT testing framework with modern DevOps practices, enabling continuous quality assurance for Adenza Capital Markets platform deployments.

## ✨ Key Features

- **🧪 CATT Integration**: Execute individual tests or full test suites via Node.js
- **🔄 CI/CD Ready**: Seamless integration with Jenkins, GitLab CI, GitHub Actions
- **📊 Result Parsing**: Intelligent parsing of CATT output with detailed reporting
- **💬 Team Notifications**: Real-time Slack and Microsoft Teams notifications
- **📈 Test History**: Track test execution history and trends
- **⚙️ Configurable**: Flexible configuration for different environments

## 💼 Business Value for Nasdaq

### Quality Assurance
- **Automated Regression**: Ensure system stability with automated test execution
- **Early Detection**: Catch issues before they reach production
- **Consistent Testing**: Standardized test execution across environments

### DevOps Excellence
- **CI/CD Integration**: Automated testing in deployment pipelines
- **Faster Feedback**: Immediate test results to development teams
- **Reduced Manual Effort**: Eliminate manual test execution

### Team Collaboration
- **Real-Time Notifications**: Keep teams informed of test results instantly
- **Visibility**: Test status visible to all stakeholders
- **Accountability**: Clear test execution history

### Compliance
- **Audit Trail**: Complete test execution history for regulatory requirements
- **Documentation**: Automated test reports for compliance documentation
- **Traceability**: Link tests to deployments and changes

## 🚀 Quick Start

### Installation

```bash
npm install
```

### Configuration

Create a `.env` file:

```env
# CATT Configuration
CATT_PATH=/path/to/catt
# Or use 'catt' if in PATH

# Slack Notifications (Optional)
SLACK_ENABLED=true
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Microsoft Teams Notifications (Optional)
TEAMS_ENABLED=true
TEAMS_WEBHOOK_URL=https://outlook.office.com/webhook/YOUR/WEBHOOK/URL

# Jenkins Integration (Optional)
JENKINS_URL=https://jenkins.nasdaq.com
JENKINS_USERNAME=your_username
JENKINS_API_TOKEN=your_token
```

### Usage

**Run a Single Test:**
```bash
node src/index.js trade-validation-test
```

**Run a Test Suite:**
```bash
node src/index.js suite:regression-suite
```

**In CI/CD Pipeline (Jenkinsfile example):**
```groovy
stage('CATT Tests') {
    steps {
        sh 'node adenza-catt-wrapper/src/index.js suite:full-regression'
    }
}
```

## 📊 Test Result Format

The wrapper provides structured test results:

```json
{
  "status": "PASSED" | "FAILED",
  "testName": "trade-validation-test",
  "passed": 10,
  "failed": 2,
  "total": 12,
  "testResults": [
    { "testName": "test-1", "status": "PASSED" },
    { "testName": "test-2", "status": "FAILED" }
  ],
  "stdout": "...",
  "stderr": "..."
}
```

## 🔔 Notification Examples

### Slack Notification
- Rich formatting with test status
- Color-coded (green for pass, red for fail)
- Summary of passed/failed/total tests
- Link to detailed test results

### Teams Notification
- Adaptive card format
- Test summary with key metrics
- Action buttons for detailed results
- Integration with Teams channels

## 🔄 CI/CD Integration

### Jenkins
```groovy
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'node adenza-catt-wrapper/src/index.js suite:regression'
            }
        }
    }
}
```

### GitLab CI
```yaml
test:
  script:
    - node adenza-catt-wrapper/src/index.js suite:regression
```

### GitHub Actions
```yaml
- name: Run CATT Tests
  run: node adenza-catt-wrapper/src/index.js suite:regression
```

## 📈 Use Cases

1. **Pre-Deployment Testing**: Automated tests before production deployment
2. **Continuous Integration**: Run tests on every code commit
3. **Regression Testing**: Full suite execution on scheduled basis
4. **Environment Validation**: Verify test environments before use

## 🔧 Customization

- **Custom Parsers**: Extend result parsing for specific CATT output formats
- **Additional Notifications**: Add email, PagerDuty, or custom notification channels
- **Test Filtering**: Filter tests by category, priority, or tags
- **Parallel Execution**: Run multiple test suites in parallel

## 📝 License

MIT License - See LICENSE file for details

---

**Built for Adenza Capital Markets Platform | Optimized for Nasdaq DevOps**
