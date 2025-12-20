# Calypso CATT Wrapper

Automated regression test suite wrapper for Calypso CATT with CI/CD integration.

## Features

- 🧪 Trigger CATT tests via Node.js
- 🔄 CI/CD pipeline integration
- 📊 Test result parsing and reporting
- 💬 Slack/Teams notifications
- 📈 Test history tracking

## Installation

```bash
npm install
```

## Usage

```bash
node src/index.js <test-name|suite:suite-name>
```

Example:
```bash
node src/index.js trade-validation-test
node src/index.js suite:regression-suite
```

## Configuration

Create a `.env` file:

```env
CATT_PATH=catt
SLACK_ENABLED=true
SLACK_WEBHOOK_URL=https://hooks.slack.com/...
TEAMS_ENABLED=false
```

## License

MIT



