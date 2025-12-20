document.addEventListener('DOMContentLoaded', () => {
  chrome.storage.local.get(['detectedErrors'], (result) => {
    const container = document.getElementById('errors-container');
    
    if (!result.detectedErrors || result.detectedErrors.length === 0) {
      container.innerHTML = '<div>No errors detected on this page.</div>';
      return;
    }

    result.detectedErrors.forEach(error => {
      const errorDiv = document.createElement('div');
      errorDiv.className = 'error-item';
      errorDiv.innerHTML = `
        <div class="error-text">${error}</div>
      `;
      container.appendChild(errorDiv);
    });
  });
});

