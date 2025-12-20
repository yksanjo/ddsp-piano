require('dotenv').config();

module.exports = {
  catt: {
    path: process.env.CATT_PATH || 'catt'
  },
  notifications: {
    slack: {
      enabled: process.env.SLACK_ENABLED === 'true',
      webhookUrl: process.env.SLACK_WEBHOOK_URL || ''
    },
    teams: {
      enabled: process.env.TEAMS_ENABLED === 'true',
      webhookUrl: process.env.TEAMS_WEBHOOK_URL || ''
    }
  },
  jenkins: {
    url: process.env.JENKINS_URL || '',
    username: process.env.JENKINS_USERNAME || '',
    apiToken: process.env.JENKINS_API_TOKEN || ''
  }
};

