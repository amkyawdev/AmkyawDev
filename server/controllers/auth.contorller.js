const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { User } = require('../models');
const authConfig = require('../config/auth.config');

const authController = {
    // Register new user
    async register(req, res) {
        try {
            const { username, email, password } = req.body;

            // Check if user exists
            const existingUser = await User.findOne({
                where: {
                    [Op.or]: [{ email }, { username }]
                }
            });

            if (existingUser) {
                return res.status(400).json({
                    success: false,
                    message: 'Username or email already exists'
                });
            }

            // Hash password
            const hashedPassword = await bcrypt.hash(password, authConfig.bcryptRounds);

            // Create user
            const user = await User.create({
                username,
                email,
                password_hash: hashedPassword
            });

            // Generate token
            const token = jwt.sign(
                { id: user.user_id, username: user.username },
                authConfig.secret,
                { expiresIn: authConfig.tokenExpire }
            );

            res.status(201).json({
                success: true,
                message: 'User registered successfully',
                token,
                user: {
                    id: user.user_id,
                    username: user.username,
                    email: user.email
                }
            });
        } catch (error) {
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    },

    // Login user
    async login(req, res) {
        try {
            const { email, password } = req.body;

            // Find user
            const user = await User.findOne({ where: { email } });
            if (!user) {
                return res.status(401).json({
                    success: false,
                    message: 'Invalid email or password'
                });
            }

            // Check password
            const isValidPassword = await bcrypt.compare(password, user.password_hash);
            if (!isValidPassword) {
                return res.status(401).json({
                    success: false,
                    message: 'Invalid email or password'
                });
            }

            // Update online status
            await user.update({ online_status: true, last_seen: new Date() });

            // Generate token
            const token = jwt.sign(
                { id: user.user_id, username: user.username },
                authConfig.secret,
                { expiresIn: authConfig.tokenExpire }
            );

            res.json({
                success: true,
                message: 'Login successful',
                token,
                user: {
                    id: user.user_id,
                    username: user.username,
                    email: user.email,
                    profile_image: user.profile_image_url
                }
            });
        } catch (error) {
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    },

    // Logout user
    async logout(req, res) {
        try {
            const user = await User.findByPk(req.userId);
            if (user) {
                await user.update({ online_status: false, last_seen: new Date() });
            }

            res.json({
                success: true,
                message: 'Logout successful'
            });
        } catch (error) {
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    },

    // Get current user profile
    async getMe(req, res) {
        try {
            const user = await User.findByPk(req.userId, {
                attributes: { exclude: ['password_hash'] }
            });

            res.json({
                success: true,
                user
            });
        } catch (error) {
            res.status(500).json({
                success: false,
                message: error.message
            });
        }
    },

    // Refresh token
    async refreshToken(req, res) {
        try {
            const { refreshToken } = req.body;
            
            if (!refreshToken) {
                return res.status(401).json({
                    success: false,
                    message: 'Refresh token required'
                });
            }

            const decoded = jwt.verify(refreshToken, authConfig.refreshSecret);
            
            const newToken = jwt.sign(
                { id: decoded.id, username: decoded.username },
                authConfig.secret,
                { expiresIn: authConfig.tokenExpire }
            );

            res.json({
                success: true,
                token: newToken
            });
        } catch (error) {
            res.status(401).json({
                success: false,
                message: 'Invalid refresh token'
            });
        }
    }
};

module.exports = authController;
