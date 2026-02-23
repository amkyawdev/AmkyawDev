const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/db.config');

const User = sequelize.define('User', {
    user_id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true
    },
    username: {
        type: DataTypes.STRING(50),
        unique: true,
        allowNull: false,
        validate: {
            len: [3, 50]
        }
    },
    email: {
        type: DataTypes.STRING(100),
        unique: true,
        allowNull: false,
        validate: {
            isEmail: true
        }
    },
    password_hash: {
        type: DataTypes.STRING(255),
        allowNull: false
    },
    profile_image_url: {
        type: DataTypes.TEXT,
        defaultValue: null
    },
    bio: {
        type: DataTypes.TEXT,
        defaultValue: null
    },
    online_status: {
        type: DataTypes.BOOLEAN,
        defaultValue: false
    },
    last_seen: {
        type: DataTypes.DATE,
        defaultValue: null
    }
}, {
    tableName: 'users',
    timestamps: true,
    createdAt: 'created_at',
    updatedAt: 'updated_at'
});

module.exports = User;
