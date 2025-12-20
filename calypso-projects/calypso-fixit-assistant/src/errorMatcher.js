const solutions = require('./solutions.json');

class ErrorMatcher {
  match(errorText) {
    const normalizedError = errorText.toLowerCase().trim();
    
    for (const solution of solutions) {
      // Check if any pattern matches
      const patterns = solution.patterns || [solution.pattern];
      
      for (const pattern of patterns) {
        if (typeof pattern === 'string') {
          if (normalizedError.includes(pattern.toLowerCase())) {
            return solution;
          }
        } else if (pattern instanceof RegExp) {
          if (pattern.test(errorText)) {
            return solution;
          }
        }
      }
    }
    
    return null;
  }

  findAllMatches(errorText) {
    const matches = [];
    const normalizedError = errorText.toLowerCase().trim();
    
    solutions.forEach(solution => {
      const patterns = solution.patterns || [solution.pattern];
      
      patterns.forEach(pattern => {
        if (typeof pattern === 'string') {
          if (normalizedError.includes(pattern.toLowerCase())) {
            matches.push(solution);
          }
        } else if (pattern instanceof RegExp) {
          if (pattern.test(errorText)) {
            matches.push(solution);
          }
        }
      });
    });
    
    return matches;
  }
}

module.exports = new ErrorMatcher();



