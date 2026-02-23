module.exports = {
    secret: process.env.JWT_SECRET,
    refreshSecret: process.env.JWT_REFRESH_SECRET,
    tokenExpire: process.env.JWT_EXPIRE,
    refreshExpire: process.env.JWT_REFRESH_EXPIRE,
    bcryptRounds: 10
};
