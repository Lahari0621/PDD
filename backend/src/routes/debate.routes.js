const express = require('express');
const router = express.Router();
const { startDebate, sendMessage, endDebate, getHistory, getDebate } = require('../controllers/debate.controller');
const { protect } = require('../middleware/auth.middleware');

router.use(protect);

router.post('/start', startDebate);
router.post('/message', sendMessage);
router.post('/end', endDebate);
router.get('/history', getHistory);
router.get('/:id', getDebate);

module.exports = router;
