const express = require('express')
const app = express()
const mongoose = require('mongoose')
const ejs = require('ejs')
const crypto = require('crypto')
const { join } = require('path')
mongoose.connect('mongodb://asocialnetwork-service-mongo:27017/prod')
app.use(express.urlencoded({ extended: true }))
app.use(express.json())
app.set('views', join(__dirname, '/views'))
app.set('view engine', 'ejs')
const cookieParser = require('cookie-parser')
const User = require('./models/user')
const Message = require('./models/message')
const Profile = require('./models/profile')
const Chatroom = require('./models/chatroom')
const Friend = require('./models/friend')
const messageRouter = require('./routers/messageRouter')
const profileRouter = require('./routers/profileRouter')
const profilePicRouter = require('./routers/profilePictureRouter')
const chatroomRouter = require('./routers/chatroomRouter')
const friendRouter = require('./routers/friendRouter')
app.use(cookieParser())
app.use(express.static(join(__dirname, '/public')))
app.use(async (req, res, next) => {
    if (req.method === 'POST' && (req.url === '/register' || req.url === '/login')) {
        next()
        return
    }
    if (req.cookies.session !== undefined) {
        const user = await User.findOne({ sessionId: req.cookies.session }).lean()
        if (!user && req.url !== '/register' && req.url !== '/login') {
            res.redirect('/register')
            return
        }
        req.user = user
    }
    next()
})
app.use('/messages', messageRouter)
app.use('/profile', profileRouter)
app.use('/profile-picture', profilePicRouter)
app.use('/chatroom', chatroomRouter)
app.use('/friends', friendRouter)
app.get('/', async (req, res, next) => {
    if (!req.user) {
        res.redirect('/login')
        return
    }
    res.page = 'home'
    try {
        const profile = await Profile.findOne({ user: req.user._id }).lean()
        const rooms = await Chatroom.find({ $or: [{ public: true }, { members: req.user._id }] }).lean()
        res.params = { userPic: profile.image, rooms }
        next()
    }
    catch (e) {
        console.log(e)
        res.status(500).send('Internal server error')
        return
    }
})
app.get('/register', (req, res, next) => {
    if (req.cookies.session !== undefined && req.user) {
        res.redirect('/')
        return
    }
    res.page = 'register'
    res.params = {}
    next()
})
app.post('/register', async (req, res, next) => {
    if (!req.body.username || !req.body.password || !req.body.confirmPassword) {
        res.status(400)
        res.page = 'register'
        res.params = { error: 'Please fill in all fields' }
        next()
        return
    }
    if (req.body.username.length > 100 || req.body.password.length > 100 || req.body.confirmPassword.length > 100) {
        res.status(400)
        res.page = 'register'
        res.params = { error: 'Username and password must be less than 100 characters' }
        next()
        return
    }
    if (req.body.password !== req.body.confirmPassword) {
        res.status(400)
        res.page = 'register'
        res.params = { error: 'Passwords do not match' }
        next()
        return
    }
    try {
        let user = await User.findOne({ userName: req.body.username }).lean()
        if (user) {
            res.status(400)
            res.page = 'register'
            res.params = { error: 'Username already exists' }
            next()
            return
        }
        const sessionId = await generateSessionId()
        const userName = req.body.username
        const password = req.body.password
        user = new User({
            sessionId,
            userName,
            password: hash(password)
        })
        const profile = new Profile({ image: Math.floor(Math.random() * 50) + 1, user: user._id, wall: [] })
        await profile.save()
        user.save().then(() => {
            res.clearCookie('session')
            res.cookie('session', sessionId, { maxAge: 900000, httpOnly: true })
            res.redirect('/')
        })
    }
    catch (e) {
        console.log(e)
        res.status(500).send('Internal server error')
        return
    }
})
async function generateSessionId () {
    return new Promise((resolve, reject) => {
        crypto.generateKey('aes', { length: 128 }, (err, key) => {
            if (err) {
                reject(err)
            } else {
                const sessionId = key.export().toString('hex')
                resolve(sessionId)
            }
        })
    })
}
function hash (password) {
    return crypto.createHash('sha256').update(password).digest('hex')
}
app.get('/login', (req, res, next) => {
    if (req.cookies.session !== undefined && req.user) {
        res.redirect('/')
        return
    }
    res.page = 'login'
    res.params = {}
    next()
})
app.post('/login', async (req, res, next) => {
    try {
        const userName = req.body.username
        const password = req.body.password
        const newSessionId = await generateSessionId()
        const user = await User.findOneAndUpdate({
            userName,
            password: hash(password)
        }, { sessionId: newSessionId }, { new: false }).lean()
        if (user) {
            res.clearCookie('session')
            res.cookie('session', newSessionId, { maxAge: 900000, httpOnly: true })
            res.redirect('/')
        } else {
            res.page = 'login'
            res.status(401)
            res.params = { error: 'Invalid username or password' }
            next()
        }
    }
    catch (e) {
        console.log(e)
        res.status(500).send('Internal server error')
        return
    }
})
app.get('/logout', (req, res) => {
    ejs.clearCache()
    res.clearCookie('session')
    res.redirect('/login')
})
app.use((req, res, next) => {
    if (!res.page) {
        next()
    }
    else {
        if (req.user) {
            res.params.userName = req.user.userName
        }
        res.render(res.page, res.params)
    }
})
async function cleanup () {
    try {
        const users = await User.find({ createdAt: { $lt: new Date(Date.now() - 30 * 60 * 1000) } }, { _id: 1 }).lean()
        await Chatroom.deleteMany({ createdAt: { $lt: new Date(Date.now() - 30 * 60 * 1000) } })
        await Profile.deleteMany({ user: { $in: users } })
        await Friend.deleteMany({ $or: [{ initiator: { $in: users } }, { recipient: { $in: users } }] })
        await Message.deleteMany({ $or: [{ sender: { $in: users } }, { recipient: { $in: users } }] })
        await User.deleteMany( { _id: { $in: users } })
    }
    catch (e) {
        console.log(e)
    }
}
setInterval(async () => {
    await cleanup()
}, 60000)

app.listen(3000, () => {
    console.log('Listening on port 3000')
})
