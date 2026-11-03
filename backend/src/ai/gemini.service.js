const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config();

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

// Model priority list — tries each in order on rate limit
const FALLBACK_MODELS = [
  'gemini-3.5-flash',
  'gemini-3.1-flash-lite',
  'gemini-2.5-flash',
  'gemini-2.5-pro',
  'gemini-2.0-flash-lite',
];

const DEBATE_SYSTEM_PROMPT = `You are an expert AI debate coach and debate partner named "Aria".

Your core responsibilities:
1. Challenge weak reasoning with intelligent counter-arguments
2. Remain respectful and educational at all times
3. Encourage critical thinking and stronger reasoning
4. Explain logical fallacies when detected, clearly and concisely
5. Generate intelligent, well-structured counter-arguments
6. Adapt to the user's skill level (beginner to expert)
7. Maintain natural conversational debate flow
8. Provide constructive feedback after each exchange

Debate style guidelines:
- Be intellectually rigorous but never condescending
- Use evidence-based reasoning when possible
- Acknowledge strong points before countering
- Ask probing Socratic questions to deepen thinking
- Keep responses focused and debate-appropriate (2-4 paragraphs max)
- Use clear logical structure: claim, evidence, reasoning

If a logical fallacy is detected in the user's argument:
1. Briefly name and explain the fallacy
2. Show why it weakens their argument
3. Suggest how they could strengthen their position
4. Continue the debate naturally

Response format:
- Start with a direct engagement of their argument
- Provide your counter-position with reasoning
- End with a challenging question or point to keep debate flowing
- Keep tone: confident, intelligent, engaging`;

const FEEDBACK_SYSTEM_PROMPT = `You are an expert debate coach providing detailed educational feedback.
Analyze the debate argument and provide:
1. Logical strength assessment (0-100)
2. Persuasion effectiveness (0-100)
3. Evidence quality assessment
4. Specific improvement suggestions
5. What was done well
6. Key logical fallacies present (if any)
Be specific, actionable, and encouraging.`;

class GeminiService {
  constructor() {
    this.conversationHistory = new Map();
    this.currentModelIndex = 0;
  }

  // Get a model instance with fallback support
  _getModel(systemInstruction = null) {
    const modelName = FALLBACK_MODELS[this.currentModelIndex] || MODEL_NAME;
    const config = {
      model: modelName,
      generationConfig: {
        temperature: 0.8,
        topK: 40,
        topP: 0.95,
        maxOutputTokens: 1024,
      },
    };
    if (systemInstruction) {
      config.systemInstruction = systemInstruction;
    }
    return genAI.getGenerativeModel(config);
  }

  // Try with fallback models on rate limit
  async _generateWithFallback(generateFn) {
    for (let i = 0; i < FALLBACK_MODELS.length; i++) {
      this.currentModelIndex = i;
      try {
        return await generateFn();
      } catch (error) {
        const isRateLimit = error.status === 429 || (error.message && error.message.includes('429'));
        const isNotFound = error.status === 404 || (error.message && error.message.includes('404'));
        
        if (isNotFound) {
          // Model doesn't exist, try next immediately
          console.log(`Model ${FALLBACK_MODELS[i]} not found, trying next...`);
          continue;
        }
        
        if (isRateLimit) {
          // Extract retry delay from error message if available
          const retryMatch = error.message && error.message.match(/retry in (\d+)/i);
          const waitMs = retryMatch ? Math.min(parseInt(retryMatch[1]) * 1000, 8000) : 2000;
          
          if (i < FALLBACK_MODELS.length - 1) {
            console.log(`Rate limit on ${FALLBACK_MODELS[i]}, waiting ${waitMs}ms then trying ${FALLBACK_MODELS[i + 1]}...`);
            await new Promise(r => setTimeout(r, waitMs));
            continue;
          }
        }
        throw error;
      }
    }
    throw new Error('All models exhausted');
  }

  // Generate debate response
  async generateDebateResponse(debateId, userMessage, context = {}) {
    try {
      const { topic, difficulty, aiPersonality, conversationHistory = [] } = context;

      const personalityModifiers = {
        socratic: 'Use the Socratic method — ask probing questions to expose flaws in reasoning.',
        aggressive: 'Be intellectually aggressive — challenge every weak point forcefully but respectfully.',
        empathetic: 'Be empathetic and understanding while still challenging weak arguments.',
        logical: 'Focus on logical analysis and structured argumentation.',
        devil_advocate: 'Always take the opposing position, even if you personally agree with the user.',
      };

      const difficultyModifiers = {
        beginner: 'Use simple, clear language. Be encouraging. Keep responses to 2-3 short paragraphs.',
        intermediate: 'Use moderate complexity. Keep responses to 2-3 paragraphs.',
        advanced: 'Use sophisticated arguments. Keep responses to 3-4 paragraphs.',
        expert: 'Use expert-level discourse. Keep responses to 3-4 paragraphs.',
      };

      const systemText = `${DEBATE_SYSTEM_PROMPT}

Topic: "${topic || 'General debate'}"
Difficulty: ${difficulty || 'intermediate'} — ${difficultyModifiers[difficulty] || difficultyModifiers.intermediate}
Personality: ${aiPersonality || 'logical'} — ${personalityModifiers[aiPersonality] || personalityModifiers.logical}

IMPORTANT: Keep your response SHORT (2-3 paragraphs max), directly relevant to what the user just said, and always end with a challenging question or counter-point.`;

      // Build valid Gemini history — must alternate user/model, start with user
      // Filter to only include messages that form valid pairs
      const rawHistory = conversationHistory.filter(m => m.content && m.content.trim());
      const validHistory = [];
      
      // Gemini requires history to alternate user → model → user → model
      // Skip the first message if it's from AI (opening statement)
      let startIdx = 0;
      if (rawHistory.length > 0 && rawHistory[0].sender === 'ai') {
        startIdx = 1; // skip AI opening
      }
      
      for (let i = startIdx; i < rawHistory.length - 1; i += 2) {
        const userMsg = rawHistory[i];
        const aiMsg = rawHistory[i + 1];
        if (userMsg && aiMsg && userMsg.sender === 'user' && aiMsg.sender === 'ai') {
          validHistory.push({ role: 'user', parts: [{ text: userMsg.content }] });
          validHistory.push({ role: 'model', parts: [{ text: aiMsg.content }] });
        }
      }

      const responseText = await this._generateWithFallback(async () => {
        // Create model fresh on each retry so it uses the current fallback model
        const model = this._getModel(systemText);
        const chat = model.startChat({ history: validHistory });
        const result = await chat.sendMessage(userMessage);
        return result.response.text();
      });

      return {
        success: true,
        content: responseText,
        model: FALLBACK_MODELS[this.currentModelIndex],
      };
    } catch (error) {
      console.error('Gemini debate response error:', error.message);
      // Smart contextual fallback based on user message content
      const msg = userMessage.toLowerCase();
      let fallback;
      
      if (msg.length < 10) {
        fallback = `"${userMessage}" — that's quite brief for a debate argument. Could you elaborate on your position? What specific point are you trying to make about ${topic || 'this topic'}?`;
      } else if (msg.includes('no evidence') || msg.includes('i don\'t know') || msg.includes('just know')) {
        fallback = `Acknowledging you have no evidence is actually an important step. In debate, claims without evidence can be dismissed without evidence. What would it take to find supporting data for your position on ${topic || 'this topic'}?`;
      } else if (msg.includes('government') || msg.includes('policy')) {
        fallback = `Government policies are complex — they can both cause and solve problems. You've raised a specific concern. Can you point to a particular policy or action that you believe is most harmful, and explain the mechanism by which it causes that harm?`;
      } else if (msg.includes('study') || msg.includes('research') || msg.includes('science')) {
        fallback = `You're citing research — good instinct. However, "studies show" without specifics is an appeal to authority. Which study? What was the sample size? What did it actually conclude? Specific citations make arguments far stronger.`;
      } else {
        fallback = `You've made a claim about "${userMessage.substring(0, 60)}..." — now let's stress-test it. What's the strongest counter-argument to your own position, and how would you respond to it?`;
      }
      
      return {
        success: false,
        content: fallback,
        error: error.message,
      };
    }
  }

  // Generate debate summary and analysis
  async generateDebateSummary(topic, messages) {
    try {
      const conversationText = messages
        .map(m => `${m.sender === 'user' ? 'User' : 'AI'}: ${m.content}`)
        .join('\n\n');

      const prompt = `Analyze this debate on "${topic}" and provide a comprehensive summary.

${conversationText}

Respond with ONLY valid JSON (no markdown, no code blocks):
{"summary":"2-3 sentence overview","winner":"user|ai|draw","winnerReason":"brief explanation","userStrengths":["strength1"],"userWeaknesses":["weakness1"],"keyInsights":["insight1","insight2"],"improvementAreas":["area1"],"logicScore":65,"persuasionScore":60,"overallScore":62,"xpEarned":75}`;

      const text = await this._generateWithFallback(async () => {
        const model = this._getModel();
        const result = await model.generateContent(prompt);
        return result.response.text().trim();
      });

      const jsonMatch = text.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        try {
          return { success: true, data: JSON.parse(jsonMatch[0]) };
        } catch (e) { /* fall through */ }
      }

      return {
        success: true,
        data: {
          summary: 'A thoughtful debate with good arguments on both sides.',
          winner: 'draw', logicScore: 65, persuasionScore: 60, overallScore: 62, xpEarned: 75,
          keyInsights: ['Good engagement with the topic', 'Room to strengthen evidence'],
          improvementAreas: ['Use more specific examples'],
          userStrengths: ['Clear position stated'], userWeaknesses: ['Could use more evidence'],
        }
      };
    } catch (error) {
      console.error('Gemini summary error:', error.message);
      return {
        success: false,
        data: {
          summary: 'Debate completed successfully.',
          winner: 'draw', logicScore: 65, persuasionScore: 60, overallScore: 62, xpEarned: 50,
          keyInsights: [], improvementAreas: [], userStrengths: [], userWeaknesses: [],
        }
      };
    }
  }

  // Generate educational feedback for a specific argument
  async generateFeedback(argument, fallacies = []) {
    try {
      const fallacyContext = fallacies.length > 0
        ? `\nDetected fallacies: ${fallacies.map(f => f.name).join(', ')}`
        : '';

      const prompt = `${FEEDBACK_SYSTEM_PROMPT}

Argument: "${argument}"${fallacyContext}

Respond with ONLY valid JSON:
{"logicScore":70,"persuasionScore":65,"clarity":75,"strengths":["point1"],"weaknesses":["point1"],"suggestions":["suggestion1"],"fallacyExplanations":[],"improvedVersion":"A stronger version would be..."}`;

      const text = await this._generateWithFallback(async () => {
        const model = this._getModel();
        const result = await model.generateContent(prompt);
        return result.response.text().trim();
      });

      const jsonMatch = text.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        try {
          return { success: true, data: JSON.parse(jsonMatch[0]) };
        } catch (e) { /* fall through */ }
      }
      return { success: true, data: { feedback: text } };
    } catch (error) {
      console.error('Gemini feedback error:', error.message);
      return { success: false, error: error.message };
    }
  }

  // Generate AI coaching tip
  async generateCoachingTip(userStats) {
    try {
      const prompt = `Based on these debate stats, give a short personalized coaching tip (2-3 sentences):
Stats: ${JSON.stringify(userStats)}
Focus on the most impactful improvement area.`;

      const tip = await this._generateWithFallback(async () => {
        const model = this._getModel();
        const result = await model.generateContent(prompt);
        return result.response.text();
      });

      return { success: true, tip };
    } catch (error) {
      return { success: true, tip: 'Focus on backing your claims with specific evidence. The strongest debaters combine logical structure with concrete examples.' };
    }
  }

  // Explain a fallacy in educational context
  async explainFallacy(fallacyType, userArgument) {
    try {
      const prompt = `Explain the "${fallacyType}" logical fallacy as it appears in this argument: "${userArgument}"

Provide:
1. Why this is a ${fallacyType} fallacy
2. How it weakens the argument
3. A corrected version
4. A memorable tip to avoid it

Keep it educational and encouraging. 2-3 paragraphs max.`;

      const explanation = await this._generateWithFallback(async () => {
        const model = this._getModel();
        const result = await model.generateContent(prompt);
        return result.response.text();
      });

      return { success: true, explanation };
    } catch (error) {
      return { success: true, explanation: `This argument contains a ${fallacyType} fallacy. Focus on addressing the argument itself with evidence rather than using logical shortcuts.` };
    }
  }
}

module.exports = new GeminiService();
