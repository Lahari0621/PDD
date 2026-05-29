const Analytics = require('../models/Analytics.model');
const Debate = require('../models/Debate.model');
const User = require('../models/User.model');
const geminiService = require('../ai/gemini.service');

const getUserAnalytics = async (req, res) => {
  try {
    const userId = req.user._id;

    // Get analytics record
    let analytics = await Analytics.findOne({ user: userId });
    if (!analytics) {
      analytics = await Analytics.create({ user: userId });
    }

    // Get recent debates
    const recentDebates = await Debate.find({ user: userId, status: 'completed' })
      .sort({ createdAt: -1 })
      .limit(10)
      .select('topic finalScore duration totalTurns winner xpEarned createdAt topicCategory');

    // Get user stats
    const user = await User.findById(userId);

    // Calculate category performance
    const categoryStats = await Debate.aggregate([
      { $match: { user: userId, status: 'completed' } },
      { $group: {
        _id: '$topicCategory',
        count: { $sum: 1 },
        avgScore: { $avg: '$finalScore' },
        wins: { $sum: { $cond: [{ $eq: ['$winner', 'user'] }, 1, 0] } },
      }},
    ]);

    // Generate coaching tip
    const coachingTip = await geminiService.generateCoachingTip({
      totalDebates: user.totalDebates,
      logicScore: user.logicScore,
      streak: user.streak,
      tier: user.tier,
    });

    // Build weekly heatmap (last 52 weeks)
    const weeklyData = analytics.weeklyActivity.slice(-52);

    // Score history (last 30 entries)
    const logicHistory = analytics.logicScoreHistory.slice(-30);
    const confidenceHistory = analytics.confidenceScoreHistory.slice(-30);

    res.json({
      success: true,
      analytics: {
        overview: {
          totalDebates: user.totalDebates,
          debatesWon: user.debatesWon,
          winRate: user.totalDebates > 0 ? Math.round((user.debatesWon / user.totalDebates) * 100) : 0,
          totalXp: user.xp,
          level: user.level,
          tier: user.tier,
          streak: user.streak,
          longestStreak: user.longestStreak,
          logicScore: user.logicScore,
          totalFallaciesDetected: user.totalFallaciesDetected,
        },
        skills: analytics.skills,
        recentDebates,
        categoryPerformance: categoryStats,
        logicScoreHistory: logicHistory,
        confidenceScoreHistory: confidenceHistory,
        weeklyActivity: weeklyData,
        fallacyBreakdown: analytics.fallacyBreakdown,
        coachingTip: coachingTip.tip,
      },
    });
  } catch (error) {
    console.error('Analytics error:', error);
    res.status(500).json({ error: 'Failed to get analytics' });
  }
};

module.exports = { getUserAnalytics };
