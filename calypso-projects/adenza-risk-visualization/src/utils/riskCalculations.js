class RiskCalculations {
  calculateVaR(positions, confidenceLevel = 0.95) {
    // Simplified VaR calculation
    const totalRisk = positions.reduce((sum, pos) => sum + (pos.riskValue || 0), 0);
    const zScore = confidenceLevel === 0.95 ? 1.96 : 2.58; // 95% or 99%
    return totalRisk * zScore;
  }

  calculatePortfolioDelta(positions) {
    return positions.reduce((sum, pos) => sum + (pos.delta || 0), 0);
  }

  calculatePortfolioGamma(positions) {
    return positions.reduce((sum, pos) => sum + (pos.gamma || 0), 0);
  }

  calculatePortfolioVega(positions) {
    return positions.reduce((sum, pos) => sum + (pos.vega || 0), 0);
  }

  calculatePortfolioTheta(positions) {
    return positions.reduce((sum, pos) => sum + (pos.theta || 0), 0);
  }

  aggregateByBook(riskData) {
    const aggregated = {};
    
    riskData.forEach(data => {
      if (!aggregated[data.book]) {
        aggregated[data.book] = {
          book: data.book,
          totalRisk: 0,
          delta: 0,
          gamma: 0,
          vega: 0,
          theta: 0,
          instruments: []
        };
      }
      
      aggregated[data.book].totalRisk += data.riskValue || 0;
      aggregated[data.book].delta += data.delta || 0;
      aggregated[data.book].gamma += data.gamma || 0;
      aggregated[data.book].vega += data.vega || 0;
      aggregated[data.book].theta += data.theta || 0;
      aggregated[data.book].instruments.push(data.instrument);
    });
    
    return Object.values(aggregated);
  }
}

module.exports = new RiskCalculations();

