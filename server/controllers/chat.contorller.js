const { Message, User, MessageImage } = require('../models');
const { Op } = require('sequelize');

const chatController = {
    // Send private message
    async sendMessage(req, res) {
        try {
            const { receiver_id, message_text, imageIds } = req.body;
            const sender_id = req.userId;

            // Create message
            const message = await Message.create({
                sender_id,
                receiver_type: 'user',
                receiver_id,
                message_text
            });

            // If there are images, associate them
            if (imageIds && imageIds.length > 0) {
                await MessageImage.update(
                    { message_id: message.message_id },
                    { where: { image_id: imageIds } }
                );
            }

            // Get full message with images
            const fullMessage = await Message.findByPk(message.message_id, {
                include: [
                    {
                        model: User,
                        as: 'sender',
                        attributes: ['user_id', 'username', 'profile_image_url']
                    },
                    {
                        model: MessageImage,
                        as: 'images'
                    }
                ]
            });

            res.status(201).json({
                success: true,
                message: fullMessage
            });
        } catch (error) {
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    },

    // Get messages between two users
    async getMessages(req, res) {
        try {
            const { userId } = req.params;
            const { page = 1, limit = 50 } = req.query;
            const offset = (page - 1) * limit;

            const messages = await Message.findAndCountAll({
                where: {
                    receiver_type: 'user',
                    [Op.or]: [
                        { sender_id: req.userId, receiver_id: userId },
                        { sender_id: userId, receiver_id: req.userId }
                    ],
                    is_deleted: false
                },
                include: [
                    {
                        model: User,
                        as: 'sender',
                        attributes: ['user_id', 'username', 'profile_image_url']
                    },
                    {
                        model: MessageImage,
                        as: 'images'
                    }
                ],
                order: [['sent_at', 'DESC']],
                limit,
                offset
            });

            res.json({
                success: true,
                messages: messages.rows,
                total: messages.count,
                currentPage: page,
                totalPages: Math.ceil(messages.count / limit)
            });
        } catch (error) {
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    },

    // Delete message
    async deleteMessage(req, res) {
        try {
            const { messageId } = req.params;

            const message = await Message.findOne({
                where: {
                    message_id: messageId,
                    sender_id: req.userId
                }
            });

            if (!message) {
                return res.status(404).json({
                    success: false,
                    message: 'Message not found or unauthorized'
                });
            }

            // Soft delete
            await message.update({ is_deleted: true });

            res.json({
                success: true,
                message: 'Message deleted successfully'
            });
        } catch (error) {
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    },

    // Edit message
    async editMessage(req, res) {
        try {
            const { messageId } = req.params;
            const { message_text } = req.body;

            const message = await Message.findOne({
                where: {
                    message_id: messageId,
                    sender_id: req.userId,
                    is_deleted: false
                }
            });

            if (!message) {
                return res.status(404).json({
                    success: false,
                    message: 'Message not found or unauthorized'
                });
            }

            await message.update({ message_text });

            res.json({
                success: true,
                message: 'Message updated successfully',
                data: message
            });
        } catch (error) {
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    }
};

module.exports = chatController;
