const Debate = require('../models/Debate.model');
const DebateMessage = require('../models/DebateMessage.model');
const User = require('../models/User.model');
const Analytics = require('../models/Analytics.model');
const geminiService = require('../ai/gemini.service');
const fallacyDetector = require('../ai/fallacy.detector');

// Start a new debate
const startDebate = async (req, res) => {
  try {
    const { topic, topicCategory, difficulty, aiPersonality, userPosition } = req.body;

    if (!topic) {
      return res.status(400).json({ error: 'Debate topic is required' });
    }

    const debate = await Debate.create({
      user: req.user._id,
      topic,
      topicCategory: topicCategory || 'custom',
      difficulty: difficulty || req.user.difficultyLevel || 'intermediate',
      aiPersonality: aiPersonality || 'logical',
      userPosition: userPosition || '',
      status: 'active',
    });

    // Generate AI opening statement
    const openingPrompt = `The debate topic is: "${topic}". ${userPosition ? `The user will argue: "${userPosition}". Take the opposing position.` : 'Start the debate with an opening statement and challenge the user to take a position.'} Begin the debate with an engaging opening statement.`;

    const aiResponse = await geminiService.generateDebateResponse(
      debate._id.toString(),
      openingPrompt,
      { topic, difficulty: debate.difficulty, aiPersonality: debate.aiPersonality, conversationHistory: [] }
    );

    // Save AI opening message
    const aiMessage = await DebateMessage.create({
      debate: debate._id,
      sender: 'ai',
      content: aiResponse.content,
      turnNumber: 1,
      model: 'gemini-1.5-flash',
    });

    debate.messages.push(aiMessage._id);
    debate.totalTurns = 1;
    await debate.save();

    res.status(201).json({
      success: true,
      debate: {
        id: debate._id,
        topic: debate.topic,
        difficulty: debate.difficulty,
        aiPersonality: debate.aiPersonality,
        status: debate.status,
        startedAt: debate.startedAt,
      },
      openingMessage: {
        id: aiMessage._id,
        sender: 'ai',
        content: aiMessage.content,
        timestamp: aiMessage.createdAt,
      },
    });
  } catch (error) {
    console.error('Start debate error:', error);
    res.status(500).json({ error: 'Failed to start debate' });
  }
};

// Send message in debate
const sendMessage = async (req, res) => {
  try {
    const { debateId, content } = req.body;

    console.log('sendMessage called - debateId:', debateId, 'userId:', req.user._id);

    if (!content || !content.trim()) {
      return res.status(400).json({ error: 'Message content is required' });
    }

    const debate = await Debate.findOne({ _id: debateId, user: req.user._id })
      .populate('messages', 'sender content createdAt');

    console.log('Debate found:', debate ? 'YES' : 'NO', 'debateId:', debateId);

    if (!debate) {
      return res.status(404).json({ error: 'Debate not found' });
    }

    if (debate.status !== 'active') {
      return res.status(400).json({ error: 'This debate is not active' });
    }

    const startTime = Date.now();

    // Detect fallacies in user message
    const fallacyResult = await fallacyDetector.detect(content);

    // Calculate scores — clamp to 0-100
    const confidenceScore = Math.min(100, Math.max(20, 100 - (fallacyResult.fallacies.length * 15) + Math.floor(Math.random() * 10)));
    const logicScore = Math.min(100, Math.max(20, 85 - (fallacyResult.fallacies.length * 20) + Math.floor(Math.random() * 15)));

    // Save user message
    const userMessage = await DebateMessage.create({
      debate: debate._id,
      sender: 'user',
      content,
      fallacies: fallacyResult.fallacies,
      hasFallacy: fallacyResult.hasFallacy,
      confidenceScore,
      logicScore,
      turnNumber: debate.totalTurns + 1,
    });

    // Build conversation history for context (Gemini needs strict user/model alternation)
    const recentMessages = debate.messages.slice(-8); // last 8 messages
    const conversationHistory = [];
    for (const m of recentMessages) {
      conversationHistory.push({
        sender: m.sender,
        content: m.content,
      });
    }

    // Generate AI response
    const aiResponse = await geminiService.generateDebateResponse(
      debate._id.toString(),
      content,
      {
        topic: debate.topic,
        difficulty: debate.difficulty,
        aiPersonality: debate.aiPersonality,
        conversationHistory,
      }
    );

    console.log('Gemini response success:', aiResponse.success, '| model:', aiResponse.model);
    if (!aiResponse.success) {
      console.error('Gemini API error:', aiResponse.error);
    }

    const processingTime = Date.now() - startTime;

    // Save AI response
    const aiMessage = await DebateMessage.create({
      debate: debate._id,
      sender: 'ai',
      content: aiResponse.content,
      turnNumber: debate.totalTurns + 2,
      processingTime,
      model: 'gemini-1.5-flash',
    });

    // Update debate
    debate.messages.push(userMessage._id, aiMessage._id);
    debate.totalTurns += 2;
    if (fallacyResult.hasFallacy) debate.userFallaciesCount += fallacyResult.fallacies.length;
    await debate.save();

    res.json({
      success: true,
      userMessage: {
        id: userMessage._id,
        sender: 'user',
        content: userMessage.content,
        fallacies: userMessage.fallacies,
        hasFallacy: userMessage.hasFallacy,
        confidenceScore: userMessage.confidenceScore,
        logicScore: userMessage.logicScore,
        timestamp: userMessage.createdAt,
      },
      aiMessage: {
        id: aiMessage._id,
        sender: 'ai',
        content: aiMessage.content,
        timestamp: aiMessage.createdAt,
        processingTime,
      },
    });
  } catch (error) {
    console.error('Send message error:', error);
    res.status(500).json({ error: 'Failed to send message' });
  }
};

// End debate
const endDebate = async (req, res) => {
  try {
    const { debateId } = req.body;

    const debate = await Debate.findOne({ _id: debateId, user: req.user._id })
      .populate('messages', 'sender content fallacies confidenceScore logicScore');

    if (!debate) {
      return res.status(404).json({ error: 'Debate not found' });
    }

    // Generate summary
    const summaryResult = await geminiService.generateDebateSummary(
      debate.topic,
      debate.messages
    );

    const summaryData = summaryResult.data || {};
    const duration = Math.floor((Date.now() - debate.startedAt) / 1000);

    // Update debate
    debate.status = 'completed';
    debate.endedAt = new Date();
    debate.duration = duration;
    debate.summary = summaryData.summary || '';
    debate.keyInsights = summaryData.keyInsights || [];
    debate.improvementAreas = summaryData.improvementAreas || [];
    debate.strengths = summaryData.userStrengths || [];
    debate.winner = summaryData.winner || 'draw';
    debate.finalScore = summaryData.overallScore || 65;
    debate.xpEarned = summaryData.xpEarned || 50;
    await debate.save();

    // Update user stats
    const user = await User.findById(req.user._id);
    user.totalDebates += 1;
    if (summaryData.winner === 'user') user.debatesWon += 1;
    user.xp += debate.xpEarned;
    user.totalFallaciesDetected += debate.userFallaciesCount;
    user.updateLevel();
    user.updateTier();
    await user.save();

    // Update analytics
    await Analytics.findOneAndUpdate(
      { user: req.user._id },
      {
        $inc: { 
          totalDebates: 1, 
          totalXpEarned: debate.xpEarned,
          totalFallaciesDetected: debate.userFallaciesCount,
        },
        $push: {
          logicScoreHistory: { date: new Date(), score: summaryData.logicScore || 65 },
          weeklyActivity: { 
            date: new Date().toISOString().split('T')[0], 
            count: 1, 
            xp: debate.xpEarned 
          },
        },
      },
      { upsert: true }
    );

    res.json({
      success: true,
      summary: {
        topic: debate.topic,
        duration,
        totalTurns: debate.totalTurns,
        winner: debate.winner,
        finalScore: debate.finalScore,
        xpEarned: debate.xpEarned,
        summary: debate.summary,
        keyInsights: debate.keyInsights,
        improvementAreas: debate.improvementAreas,
        strengths: debate.strengths,
        logicScore: summaryData.logicScore || 65,
        persuasionScore: summaryData.persuasionScore || 60,
      },
    });
  } catch (error) {
    console.error('End debate error:', error);
    res.status(500).json({ error: 'Failed to end debate' });
  }
};

// Get debate history
const getHistory = async (req, res) => {
  try {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 10;
    const skip = (page - 1) * limit;

    const debates = await Debate.find({ user: req.user._id })
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(limit)
      .select('-messages');

    const total = await Debate.countDocuments({ user: req.user._id });

    res.json({
      success: true,
      debates,
      pagination: { page, limit, total, pages: Math.ceil(total / limit) },
    });
  } catch (error) {
    res.status(500).json({ error: 'Failed to get debate history' });
  }
};

// Get single debate with messages
const getDebate = async (req, res) => {
  try {
    const debate = await Debate.findOne({ _id: req.params.id, user: req.user._id })
      .populate('messages');

    if (!debate) {
      return res.status(404).json({ error: 'Debate not found' });
    }

    res.json({ success: true, debate });
  } catch (error) {
    res.status(500).json({ error: 'Failed to get debate' });
  }
};

module.exports = { startDebate, sendMessage, endDebate, getHistory, getDebate };
