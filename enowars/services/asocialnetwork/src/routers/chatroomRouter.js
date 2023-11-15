const express = require('express')
const router = express.Router()
const Chatroom = require('../models/chatroom')
const Profile = require('../models/profile')
const crypto = require('crypto')
router.use(async (req, res, next) => {
    if (!req.user) {
        res.redirect('/login')
        return
    }
    next()
})
router.get('/:roomId', async (req, res, next) => {
    try {
        const chatroom = await Chatroom.findOne({ id: req.params.roomId })
        if (!chatroom) {
            res.redirect('/')
            return
        }
        if (!chatroom.members.includes(req.user._id)) {
            chatroom.members.push(req.user._id)
            await chatroom.save()
        }
        res.page = 'chatroom'
        if (chatroom.messages.length > 0) {
            res.params = { chatroom, lastMessage: chatroom.messages[chatroom.messages.length - 1].date.valueOf() }
        } else {
            res.params = { chatroom, lastMessage: 0 }
        }
        next()
    } catch (e) {
        console.log(e)
        res.status(500).send('Internal server error')
    }
})
async function newMessagesAvailable (roomId, lastMessageDate) {
    const chatroom = await Chatroom.findOne({ id: roomId }).lean()
    if (!chatroom) {
        return false
    }
    if (chatroom.messages.length === 0) {
        return false
    }
    return lastMessageDate.getTime() < chatroom.messages[chatroom.messages.length - 1].date.getTime()
}
async function getNewMessages (roomId, lastMessageDate) {
    const chatroom = await Chatroom.findOne({ id: roomId }).lean()
    const newMessages = []
    if (chatroom) {
        for (let i = 0; i < chatroom.messages.length; i++) {
            if (chatroom.messages[i].date.getTime() > lastMessageDate.getTime()) {
                const message = {
                    message: chatroom.messages[i].message,
                    author: chatroom.messages[i].author,
                    date: chatroom.messages[i].date,
                    user: {
                        userName: chatroom.messages[i].author.userName,
                        avatar: '/assets/profile-pics/' + chatroom.messages[i].author.image + '.jpg'
                    }
                }
                newMessages.push(message)
            }
        }
    }
    return newMessages
}
function waitUntilNewMessagesOrTimeout (callback, roomId, lastMessageDate) {
    const timeout = setTimeout(function () {
        // Timeout occurred, return empty response
        callback([])
    }, 30000) // 30 seconds

    async function checkForNewMessages () {
        // Check for new messages
        if (await newMessagesAvailable(roomId, lastMessageDate)) {
            // New messages available, return them
            clearTimeout(timeout)
            callback(await getNewMessages(roomId, lastMessageDate))
        } else {
            // No new messages, check again in a short delay
            setTimeout(checkForNewMessages, 1000)
        }
    }

    // Start checking for new messages
    checkForNewMessages()
}
router.get('/:roomId/messages/:lastMessageTime', async (req, res) => {
    try {
        const chatroom = await Chatroom.findOne({ id: req.params.roomId })
        if (!chatroom) {
            res.status(400).send('Chatroom not found')
            return
        }
        if (!req.params.lastMessageTime) {
            res.status(400).send('lastMessageTime is required')
            return
        }
        chatroom.users.push(req.user._id)
        await chatroom.save()
        waitUntilNewMessagesOrTimeout(async function (newMessages) {
            // Return new messages to the client
            const chatroom = (await Chatroom.findOne({ id: req.params.roomId }))
            if (!chatroom) {
                return
            }
            chatroom.users.splice(chatroom.users.indexOf(req.user._id), 1)
            chatroom.save()
            if (!res.headersSent) { res.json(newMessages) }
        }, req.params.roomId, new Date(Number.parseInt(req.params.lastMessageTime)))
    } catch (e) {
        console.log(e)
        res.status(500).send('Internal server error')
    }
})
router.post('/', async (req, res) => {
    try {
        let chatroom = await Chatroom.findOne({ id: crypto.createHash('sha256').update(req.body.roomname).digest('hex') }).lean()
        if (typeof req.body.roomname !== 'string') {
            res.status(400).send('Room Name must be a string')
            return
        }
        if (!req.body.roomname) {
            res.status(400).send('Room Name is required')
            return
        }
        if (req.body.roomname.length > 20) {
            res.status(400).send('Room Name must be less than 20 characters')
            return
        }
        if (!req.body.public) {
            res.status(400).send('public is required')
            return
        }
        if (req.body.public !== 'true' && req.body.public !== 'false') {
            res.status(400).send('public must be true or false')
            return
        }
        if (!chatroom) {
            chatroom = new Chatroom({
                name: req.body.roomname,
                users: [],
                messages: [],
                members: [],
                public: req.body.public,
                id: crypto.createHash('sha256').update(req.body.roomname).digest('hex')
            })
            await chatroom.save()
            res.status(200).send(chatroom.id)
        } else {
            res.status(400).send('Room already exists')
        }
    } catch (e) {
        console.log(e)
        res.status(500).send('Internal server error')
    }
})
router.post('/:roomId/messages', async (req, res) => {
    try {
        const chatroom = await Chatroom.findOne({ id: req.params.roomId })
        if (!chatroom) {
            res.send('Chatroom does not exist')
            return
        }
        if (!req.body.message) {
            res.send('Message is required')
            return
        }
        if (req.body.message.length > 1000) {
            res.send('Message must be less than 1000 characters')
            return
        }
        const message = {
            message: req.body.message,
            author: { userName: req.user.userName, image: (await Profile.findOne({ user: req.user._id }).lean()).image },
            date: Date.now()
        }
        chatroom.messages.push(message)
        await chatroom.save()
        res.redirect('/chatroom/' + req.params.roomId)
    } catch (e) {
        console.log(e)
        res.status(500).send('Internal server error')
    }
})
module.exports = router
