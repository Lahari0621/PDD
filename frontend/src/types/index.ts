export interface User {
  id: string
  username: string
  email: string
  avatar?: string
  bio?: string
  xp: number
  level: number
  tier: 'Bronze' | 'Silver' | 'Gold' | 'Platinum' | 'Diamond'
  streak: number
  longestStreak: number
  plan: 'free' | 'pro' | 'education'
  role: 'user' | 'admin' | 'educator'
  difficultyLevel: 'beginner' | 'intermediate' | 'advanced' | 'expert'
  totalDebates: number
  debatesWon?: number
  logicScore: number
  totalFallaciesDetected?: number
  achievements?: Achievement[]
  preferredTopics?: string[]
}

export interface Debate {
  id: string
  topic: string
  topicCategory: string
  difficulty: string
  aiPersonality: string
  status: 'active' | 'paused' | 'completed' | 'abandoned'
  totalTurns: number
  finalScore?: number
  winner?: 'user' | 'ai' | 'draw' | null
  summary?: string
  xpEarned?: number
  startedAt: string
  endedAt?: string
  duration?: number
  createdAt: string
}

export interface DebateMessage {
  id: string
  sender: 'user' | 'ai'
  content: string
  fallacies?: Fallacy[]
  hasFallacy?: boolean
  confidenceScore?: number
  logicScore?: number
  timestamp: string
  processingTime?: number
}

export interface Fallacy {
  type: string
  name: string
  description: string
  highlightedText?: string
  startIndex?: number
  endIndex?: number
  confidence: number
  severity?: 'low' | 'medium' | 'high'
  color?: string
  explanation?: string
  correction?: string
  detectionMethod?: string
}

export interface FallacyLibraryItem {
  type: string
  name: string
  category: string
  description: string
  shortDescription: string
  example: string
  correctedExample: string
  severity: 'low' | 'medium' | 'high'
  color: string
  icon: string
  tips?: string[]
}

export interface Topic {
  id: string
  title: string
  category: string
  difficulty: string
  icon: string
  tags: string[]
  debateCount: number
  description?: string
}

export interface Achievement {
  id: string
  name: string
  description: string
  icon: string
  unlockedAt: string
}

export interface Analytics {
  overview: {
    totalDebates: number
    debatesWon: number
    winRate: number
    totalXp: number
    level: number
    tier: string
    streak: number
    longestStreak: number
    logicScore: number
    totalFallaciesDetected: number
  }
  skills: {
    logic: number
    persuasion: number
    evidence: number
    clarity: number
    rebuttal: number
    structure: number
  }
  recentDebates: Debate[]
  categoryPerformance: Array<{ _id: string; count: number; avgScore: number; wins: number }>
  logicScoreHistory: Array<{ date: string; score: number }>
  weeklyActivity: Array<{ date: string; count: number; xp: number }>
  fallacyBreakdown: Array<{ type: string; count: number }>
  coachingTip: string
}

export interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
}

export interface DebateState {
  currentDebate: Debate | null
  messages: DebateMessage[]
  isTyping: boolean
  isLoading: boolean
  activeFallacy: Fallacy | null
}
