const AdenzaClient = require('./services/AdenzaClient');
const legalEntityValidator = require('./validators/legalEntityValidator');
const bookValidator = require('./validators/bookValidator');
const portfolioValidator = require('./validators/portfolioValidator');
const reportGenerator = require('./reporters/reportGenerator');
const logger = require('./utils/logger');

class HealthCheck {
  constructor() {
    this.issues = [];
    this.stats = {
      legalEntities: { total: 0, valid: 0, invalid: 0 },
      books: { total: 0, valid: 0, invalid: 0 },
      portfolios: { total: 0, valid: 0, invalid: 0 }
    };
  }

  async run() {
    logger.info('Starting static data health check...');

    try {
      // Check Legal Entities
      await this.checkLegalEntities();

      // Check Books
      await this.checkBooks();

      // Check Portfolios
      await this.checkPortfolios();

      // Generate report
      const report = reportGenerator.generate(this.issues, this.stats);
      
      logger.info('Health check completed');
      return {
        issues: this.issues,
        stats: this.stats,
        report: report,
        score: this.calculateScore()
      };
    } catch (error) {
      logger.error('Health check failed', error);
      throw error;
    }
  }

  async checkLegalEntities() {
    logger.info('Checking Legal Entities...');
    const entities = await AdenzaClient.getLegalEntities();

    this.stats.legalEntities.total = entities.length;

    entities.forEach(entity => {
      const validation = legalEntityValidator.validate(entity);
      if (validation.valid) {
        this.stats.legalEntities.valid++;
      } else {
        this.stats.legalEntities.invalid++;
        this.issues.push({
          type: 'legal_entity',
          entity: entity.id || entity.name,
          issues: validation.errors
        });
      }
    });
  }

  async checkBooks() {
    logger.info('Checking Books...');
    const books = await AdenzaClient.getBooks();

    this.stats.books.total = books.length;

    books.forEach(book => {
      const validation = bookValidator.validate(book);
      if (validation.valid) {
        this.stats.books.valid++;
      } else {
        this.stats.books.invalid++;
        this.issues.push({
          type: 'book',
          book: book.id || book.name,
          issues: validation.errors
        });
      }
    });
  }

  async checkPortfolios() {
    logger.info('Checking Portfolios...');
    const portfolios = await AdenzaClient.getPortfolios();

    this.stats.portfolios.total = portfolios.length;

    portfolios.forEach(portfolio => {
      const validation = portfolioValidator.validate(portfolio);
      if (validation.valid) {
        this.stats.portfolios.valid++;
      } else {
        this.stats.portfolios.invalid++;
        this.issues.push({
          type: 'portfolio',
          portfolio: portfolio.id || portfolio.name,
          issues: validation.errors
        });
      }
    });
  }

  calculateScore() {
    const total = this.stats.legalEntities.total + 
                  this.stats.books.total + 
                  this.stats.portfolios.total;
    const invalid = this.stats.legalEntities.invalid + 
                    this.stats.books.invalid + 
                    this.stats.portfolios.invalid;

    if (total === 0) return 100;
    return Math.round(((total - invalid) / total) * 100);
  }
}

module.exports = new HealthCheck();

