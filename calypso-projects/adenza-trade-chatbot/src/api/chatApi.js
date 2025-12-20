const express = require('express');
const chatbot = require('../chatbot/chatbot');
const router = express.Router();

router.post('/chat', async (req, res) => {
  try {
    const { query } = req.body;
    
    if (!query) {
      return res.status(400).json({ error: 'Query is required' });
    }

    const response = await chatbot.processQuery(query);
    res.json({ response });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get('/history', (req, res) => {
  const history = chatbot.getHistory();
  res.json({ history });
});

router.delete('/history', (req, res) => {
  chatbot.clearHistory();
  res.json({ message: 'History cleared' });
});

module.exports = router;

