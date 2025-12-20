const axios = require('axios');
const logger = require('../utils/logger');

class TeamsNotifier {
  constructor(webhookUrl) {
    this.webhookUrl = webhookUrl;
  }

  async sendTestResults(results) {
    try {
      const message = this.formatMessage(results);
      
      await axios.post(this.webhookUrl, message);

      logger.info('Teams notification sent');
    } catch (error) {
      logger.error('Failed to send Teams notification', error);
      throw error;
    }
  }

  formatMessage(results) {
    const statusEmoji = results.status === 'PASSED' ? '✅' : '❌';
    const themeColor = results.status === 'PASSED' ? '00ff00' : 'ff0000';

    return {
      '@type': 'MessageCard',
      '@context': 'https://schema.org/extensions',
      themeColor: themeColor,
      summary: `CATT Test Results: ${results.testName || results.suiteName}`,
      sections: [
        {
          activityTitle: `${statusEmoji} CATT Test Results`,
          facts: [
            {
              name: 'Test Name',
              value: results.testName || results.suiteName
            },
            {
              name: 'Status',
              value: results.status
            },
            {
              name: 'Passed',
              value: (results.passed || 0).toString()
            },
            {
              name: 'Failed',
              value: (results.failed || 0).toString()
            },
            {
              name: 'Total',
              value: (results.total || 0).toString()
            }
          ]
        }
      ]
    };
  }
}

module.exports = TeamsNotifier;

