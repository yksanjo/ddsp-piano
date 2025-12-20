const axios = require('axios');
const logger = require('../utils/logger');

class SlackNotifier {
  constructor(webhookUrl) {
    this.webhookUrl = webhookUrl;
  }

  async sendTestResults(results) {
    try {
      const message = this.formatMessage(results);
      
      await axios.post(this.webhookUrl, {
        text: 'CATT Test Results',
        blocks: message.blocks
      });

      logger.info('Slack notification sent');
    } catch (error) {
      logger.error('Failed to send Slack notification', error);
      throw error;
    }
  }

  formatMessage(results) {
    const statusEmoji = results.status === 'PASSED' ? '✅' : '❌';
    const color = results.status === 'PASSED' ? 'good' : 'danger';

    const blocks = [
      {
        type: 'header',
        text: {
          type: 'plain_text',
          text: `${statusEmoji} CATT Test Results: ${results.testName || results.suiteName}`
        }
      },
      {
        type: 'section',
        fields: [
          {
            type: 'mrkdwn',
            text: `*Status:* ${results.status}`
          },
          {
            type: 'mrkdwn',
            text: `*Passed:* ${results.passed || 0}`
          },
          {
            type: 'mrkdwn',
            text: `*Failed:* ${results.failed || 0}`
          },
          {
            type: 'mrkdwn',
            text: `*Total:* ${results.total || 0}`
          }
        ]
      }
    ];

    if (results.error) {
      blocks.push({
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: `*Error:*\n\`\`\`${results.error}\`\`\``
        }
      });
    }

    return { blocks };
  }
}

module.exports = SlackNotifier;

