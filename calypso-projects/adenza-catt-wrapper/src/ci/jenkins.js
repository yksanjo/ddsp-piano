const axios = require('axios');
const logger = require('../utils/logger');

class JenkinsIntegration {
  constructor(jenkinsUrl, username, apiToken) {
    this.jenkinsUrl = jenkinsUrl;
    this.username = username;
    this.apiToken = apiToken;
  }

  async triggerJob(jobName, parameters = {}) {
    try {
      const url = `${this.jenkinsUrl}/job/${jobName}/buildWithParameters`;
      const auth = Buffer.from(`${this.username}:${this.apiToken}`).toString('base64');

      const response = await axios.post(url, parameters, {
        headers: {
          'Authorization': `Basic ${auth}`,
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });

      logger.info(`Jenkins job triggered: ${jobName}`);
      return response.data;
    } catch (error) {
      logger.error(`Failed to trigger Jenkins job: ${jobName}`, error);
      throw error;
    }
  }

  async getJobStatus(jobName, buildNumber) {
    try {
      const url = `${this.jenkinsUrl}/job/${jobName}/${buildNumber}/api/json`;
      const auth = Buffer.from(`${this.username}:${this.apiToken}`).toString('base64');

      const response = await axios.get(url, {
        headers: {
          'Authorization': `Basic ${auth}`
        }
      });

      return response.data;
    } catch (error) {
      logger.error(`Failed to get Jenkins job status: ${jobName}`, error);
      throw error;
    }
  }
}

module.exports = JenkinsIntegration;

