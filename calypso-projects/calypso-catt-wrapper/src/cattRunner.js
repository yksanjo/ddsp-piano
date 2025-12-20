const { exec } = require('child_process');
const { promisify } = require('util');
const fs = require('fs').promises;
const path = require('path');
const logger = require('./utils/logger');

const execAsync = promisify(exec);

class CATTRunner {
  constructor(cattPath) {
    this.cattPath = cattPath || process.env.CATT_PATH || 'catt';
  }

  async runTest(testName, options = {}) {
    try {
      logger.info(`Running CATT test: ${testName}`);
      
      const command = `${this.cattPath} run ${testName} ${options.args || ''}`;
      const { stdout, stderr } = await execAsync(command, {
        cwd: options.workingDirectory,
        timeout: options.timeout || 300000 // 5 minutes default
      });

      const result = this.parseResults(stdout, stderr);
      result.testName = testName;
      result.command = command;

      logger.info(`Test ${testName} completed: ${result.status}`);
      return result;
    } catch (error) {
      logger.error(`CATT test failed: ${testName}`, error);
      return {
        testName,
        status: 'FAILED',
        error: error.message,
        stdout: error.stdout,
        stderr: error.stderr
      };
    }
  }

  async runTestSuite(suiteName, options = {}) {
    try {
      logger.info(`Running CATT test suite: ${suiteName}`);
      
      const command = `${this.cattPath} suite ${suiteName} ${options.args || ''}`;
      const { stdout, stderr } = await execAsync(command, {
        cwd: options.workingDirectory,
        timeout: options.timeout || 600000 // 10 minutes default
      });

      const result = this.parseSuiteResults(stdout, stderr);
      result.suiteName = suiteName;
      result.command = command;

      logger.info(`Suite ${suiteName} completed: ${result.passed}/${result.total} tests passed`);
      return result;
    } catch (error) {
      logger.error(`CATT suite failed: ${suiteName}`, error);
      return {
        suiteName,
        status: 'FAILED',
        error: error.message,
        passed: 0,
        total: 0
      };
    }
  }

  parseResults(stdout, stderr) {
    // Parse CATT output
    const lines = stdout.split('\n');
    let status = 'UNKNOWN';
    let passed = 0;
    let failed = 0;
    let total = 0;

    lines.forEach(line => {
      if (line.includes('PASSED') || line.includes('SUCCESS')) {
        status = 'PASSED';
        passed++;
        total++;
      } else if (line.includes('FAILED') || line.includes('ERROR')) {
        status = 'FAILED';
        failed++;
        total++;
      } else if (line.match(/\d+\s+test/)) {
        const match = line.match(/(\d+)\s+test/);
        if (match) total = parseInt(match[1]);
      }
    });

    return {
      status: status === 'UNKNOWN' ? (failed > 0 ? 'FAILED' : 'PASSED') : status,
      passed,
      failed,
      total,
      stdout,
      stderr
    };
  }

  parseSuiteResults(stdout, stderr) {
    const result = this.parseResults(stdout, stderr);
    const lines = stdout.split('\n');
    const testResults = [];

    lines.forEach((line, index) => {
      if (line.includes('Test:')) {
        const testName = line.split('Test:')[1]?.trim();
        const nextLine = lines[index + 1];
        const status = nextLine?.includes('PASSED') ? 'PASSED' : 
                      nextLine?.includes('FAILED') ? 'FAILED' : 'UNKNOWN';
        
        if (testName) {
          testResults.push({ testName, status });
        }
      }
    });

    return {
      ...result,
      testResults
    };
  }
}

module.exports = CATTRunner;



