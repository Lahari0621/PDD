const { Server } = require('socket.io');
const jwt = require('jsonwebtoken');
const User = require('../models/User.model');
const geminiService = require('../ai/gemini.service');
const fallacyDetector = require('../ai/fallacy.detector');

let io;

const initializeSocket = (server) => {
  io = new Server(server, {
    cors: {
      origin: [process.env.CLIENT_URL, 'http://localhost:5173'],
      methods: ['GET', 'POST'],
      credentials: true,
    },
    pingTimeout: 60000,
  });

  // Auth middleware for socket
  io.use(async (socket, next) => {
    try {
      const token = socket.handshake.auth.token;
      if (!token) {
        return next(new Error('Authentication required'));
      }
      const decoded = jwt.verify(token, process.env.JWT_SECRET);
      const user = await User.findById(decoded.id).select('-password');
      if (!user) return next(new Error('User not found'));
      socket.user = user;
      next();
    } catch (error) {
      next(new Error('Invalid token'));
    }
  });

  io.on('connection', (socket) => {
    console.log(`🔌 User connected: ${socket.user.username} (${socket.id})`);

    // Join debate room
    socket.on('join_debate', ({ debateId }) => {
      socket.join(`debate:${debateId}`);
      console.log(`${socket.user.username} joined debate: ${debateId}`);
    });

    // Handle real-time message
    socket.on('send_message', async ({ debateId, content, conversationHistory = [] }) => {
      try {
        // Emit typing indicator
        socket.to(`debate:${debateId}`).emit('typing_started', { sender: 'ai' });
        socket.emit('typing_started', { sender: 'ai' });

        // Detect fallacies
        const fallacyResult = await fallacyDetector.detect(content);

        // Emit fallacy detection immediately
        if (fallacyResult.hasFallacy) {
          socket.emit('fallacy_detected', {
            fallacies: fallacyResult.fallacies,
            messageContent: content,
          });
        }

        // Generate AI response
        const aiResponse = await geminiService.generateDebateResponse(
          debateId,
          content,
          { conversationHistory }
        );

        // Stop typing indicator
        socket.emit('typing_stopped', { sender: 'ai' });

        // Emit AI response
        socket.emit('ai_response', {
          content: aiResponse.content,
          timestamp: new Date().toISOString(),
          fallacies: fallacyResult.fallacies,
          hasFallacy: fallacyResult.hasFallacy,
        });

      } catch (error) {
        console.error('Socket message error:', error);
        socket.emit('typing_stopped', { sender: 'ai' });
        socket.emit('ai_response', {
          content: "I encountered an issue processing your argument. Please try again.",
          timestamp: new Date().toISOString(),
          error: true,
        });
      }
    });

    // Typing indicator from user
    socket.on('typing', ({ debateId, isTyping }) => {
      socket.to(`debate:${debateId}`).emit(isTyping ? 'typing_started' : 'typing_stopped', {
        sender: 'user',
        userId: socket.user._id,
      });
    });

    // Pause debate
    socket.on('pause_debate', ({ debateId }) => {
      io.to(`debate:${debateId}`).emit('debate_paused', { debateId });
    });

    // End debate
    socket.on('end_debate', async ({ debateId, messages }) => {
      try {
        const summaryResult = await geminiService.generateDebateSummary(
          'Debate Topic',
          messages || []
        );
        
        io.to(`debate:${debateId}`).emit('debate_summary', {
          debateId,
          summary: summaryResult.data,
        });
      } catch (error) {
        socket.emit('debate_summary', { debateId, error: 'Failed to generate summary' });
      }
    });

    socket.on('disconnect', () => {
      console.log(`🔌 User disconnected: ${socket.user.username}`);
    });
  });

  return io;
};

const getIO = () => {
  if (!io) throw new Error('Socket.io not initialized');
  return io;
};

module.exports = { initializeSocket, getIO };
