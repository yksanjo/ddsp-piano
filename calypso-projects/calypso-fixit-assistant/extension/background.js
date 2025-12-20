chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'errors_detected') {
    chrome.storage.local.set({
      detectedErrors: message.errors,
      lastUpdate: new Date().toISOString()
    });
  }
});



