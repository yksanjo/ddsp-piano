const errorMatcher = require('../src/errorMatcher');
const solutions = require('../src/solutions.json');

// Monitor for error messages on the page
function detectErrors() {
  const errorSelectors = [
    '.error',
    '.error-message',
    '[class*="error"]',
    '[id*="error"]',
    '.alert-danger',
    '.notification-error'
  ];

  const errors = [];
  errorSelectors.forEach(selector => {
    const elements = document.querySelectorAll(selector);
    elements.forEach(el => {
      const text = el.textContent || el.innerText;
      if (text && text.trim().length > 0) {
        errors.push({
          element: el,
          text: text.trim(),
          html: el.innerHTML
        });
      }
    });
  });

  return errors;
}

// Match errors with solutions
function findSolutions(errors) {
  return errors.map(error => {
    const match = errorMatcher.match(error.text);
    return {
      error: error.text,
      solution: match,
      element: error.element
    };
  });
}

// Inject fix suggestions
function injectSuggestions(matchedErrors) {
  matchedErrors.forEach(({ error, solution, element }) => {
    if (solution) {
      const suggestionDiv = document.createElement('div');
      suggestionDiv.className = 'calypso-fixit-suggestion';
      suggestionDiv.innerHTML = `
        <div class="fixit-header">
          <strong>Fix-It Assistant Suggestion:</strong>
        </div>
        <div class="fixit-message">${solution.message}</div>
        ${solution.link ? `<a href="${solution.link}" target="_blank" class="fixit-link">Fix Now</a>` : ''}
        ${solution.command ? `<div class="fixit-command">${solution.command}</div>` : ''}
      `;
      
      // Insert after the error element
      element.parentNode.insertBefore(suggestionDiv, element.nextSibling);
    }
  });
}

// Main execution
function runFixItAssistant() {
  const errors = detectErrors();
  if (errors.length > 0) {
    const matchedErrors = findSolutions(errors);
    injectSuggestions(matchedErrors);
    
    // Send to background script for storage
    chrome.runtime.sendMessage({
      type: 'errors_detected',
      count: errors.length,
      errors: matchedErrors.map(e => e.error)
    });
  }
}

// Run on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', runFixItAssistant);
} else {
  runFixItAssistant();
}

// Monitor for dynamically added errors
const observer = new MutationObserver(() => {
  runFixItAssistant();
});

observer.observe(document.body, {
  childList: true,
  subtree: true
});



