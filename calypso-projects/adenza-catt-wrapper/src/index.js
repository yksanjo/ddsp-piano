#!/usr/bin/env node

const CATTRunner = require('./cattRunner');
const SlackNotifier = require('./notifications/slack');
const TeamsNotifier = require('./notifications/teams');
const config = require('./config/config');
const logger = require('./utils/logger');

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length < 1) {
    console.log('Usage: node src/index.js <test-name|suite-name> [options]');
    console.log('  test-name: Name of CATT test to run');
    console.log('  suite-name: Name of CATT test suite to run (prefix with "suite:")');
    process.exit(1);
  }

  const testName = args[0];
  const isSuite = testName.startsWith('suite:');
  const actualTestName = isSuite ? testName.replace('suite:', '') : testName;

  try {
    const runner = new CATTRunner();
    let results;

    if (isSuite) {
      results = await runner.runTestSuite(actualTestName);
    } else {
      results = await runner.runTest(actualTestName);
    }

    // Send notifications
    if (config.notifications.slack.enabled && config.notifications.slack.webhookUrl) {
      const slack = new SlackNotifier(config.notifications.slack.webhookUrl);
      await slack.sendTestResults(results);
    }

    if (config.notifications.teams.enabled && config.notifications.teams.webhookUrl) {
      const teams = new TeamsNotifier(config.notifications.teams.webhookUrl);
      await teams.sendTestResults(results);
    }

    // Exit with appropriate code
    process.exit(results.status === 'PASSED' ? 0 : 1);
  } catch (error) {
    logger.error('CATT wrapper failed', error);
    console.error('Error:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { main };

