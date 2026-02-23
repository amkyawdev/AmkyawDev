const express = require('express');
const router = express.Router();
const chatController = require('../controllers/chat.controller');
const authMiddleware = require('../middleware/auth.middleware');

router.use(authMiddleware);

router.post('/message', chatController.sendMessage);
router.get('/messages/:userId', chatController.getMessages);
router.delete('/message/:messageId', chatController.deleteMessage);
router.put('/message/:messageId', chatController.editMessage);

module.exports = router;
