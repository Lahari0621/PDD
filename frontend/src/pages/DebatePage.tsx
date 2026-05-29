import React, { useState, useEffect, useRef } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Brain, Send, Pause, Play, Square, Mic, MicOff, AlertTriangle, ChevronDown, Zap, ArrowLeft, Loader2, MessageSquare } from 'lucide-react'
import { useDebateStore } from '../store/debateStore'
import { useAuthStore } from '../store/authStore'
import { debateService } from '../services/debate.service'
import { AI_PERSONALITIES, DIFFICULTY_COLORS } from '../constants'
import toast from 'react-hot-toast'
import GradientOrbs from '../components/animations/GradientOrbs'
import type { DebateMessage, Fallacy } from '../types'

function FallacyTooltip({ fallacy, onClose }: { fallacy: Fallacy; onClose: () => void }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9, y: 10 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.9, y: 10 }}
      className="absolute z-50 bottom-full left-0 mb-2 w-72 glass-dark rounded-xl p-4 border shadow-glass"
      style={{ borderColor: `${fallacy.color}40` }}
    >
      <div className="flex items-center justify-between mb-2">
        <span className="font-bold text-sm" style={{ color: fallacy.color }}>{fallacy.name}</span>
        <button onClick={onClose} className="text-slate-500 hover:text-white text-xs">✕</button>
      </div>
      <p className="text-slate-300 text-xs leading-relaxed mb-2">{fallacy.description}</p>
      <div className="flex items-center gap-2">
        <div className="text-xs text-slate-500">Confidence:</div>
        <div className="flex-1 h-1 bg-white/10 rounded-full overflow-hidden">
          <div className="h-full rounded-full" style={{ width: `${Math.round(fallacy.confidence * 100)}%`, background: fallacy.color }} />
        </div>
        <div className="text-xs font-bold" style={{ color: fallacy.color }}>{Math.round(fallacy.confidence * 100)}%</div>
      </div>
    </motion.div>
  )
}

function MessageBubble({ message, onFallacyClick }: { message: DebateMessage; onFallacyClick: (f: Fallacy) => void }) {
  const isUser = message.sender === 'user'
  const [activeFallacy, setActiveFallacy] = useState<Fallacy | null>(null)

  const renderContent = () => {
    if (!message.hasFallacy || !message.fallacies?.length) return <span>{message.content}</span>
    let content = message.content
    const parts: React.ReactElement[] = []
    let lastIndex = 0
    const sortedFallacies = [...message.fallacies].sort((a, b) => (a.startIndex || 0) - (b.startIndex || 0))

    sortedFallacies.forEach((f, i) => {
      if (f.startIndex !== undefined && f.endIndex !== undefined) {
        if (f.startIndex > lastIndex) {
          parts.push(<span key={`text-${i}`}>{content.slice(lastIndex, f.startIndex)}</span>)
        }
        parts.push(
          <span key={`fallacy-${i}`} className="relative inline">
            <span
              className="fallacy-highlight cursor-pointer"
              style={{ borderBottomColor: f.color }}
              onClick={() => setActiveFallacy(activeFallacy?.type === f.type ? null : f)}
            >
              {content.slice(f.startIndex, f.endIndex)}
            </span>
            <AnimatePresence>
              {activeFallacy?.type === f.type && (
                <FallacyTooltip fallacy={f} onClose={() => setActiveFallacy(null)} />
              )}
            </AnimatePresence>
          </span>
        )
        lastIndex = f.endIndex
      }
    })
    if (lastIndex < content.length) parts.push(<span key="text-end">{content.slice(lastIndex)}</span>)
    return <>{parts}</>
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 15, scale: 0.97 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.35, type: 'spring', stiffness: 200 }}
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}
    >
      <div className={`max-w-[80%] ${isUser ? 'items-end' : 'items-start'} flex flex-col`}>
        {!isUser && (
          <div className="flex items-center gap-2 mb-1.5">
            <div className="w-6 h-6 rounded-full bg-gradient-to-br from-primary-600 to-indigo-500 flex items-center justify-center">
              <Brain className="w-3 h-3 text-white" />
            </div>
            <span className="text-xs text-slate-500 font-medium">Aria — AI Coach</span>
          </div>
        )}
        <div className={`relative px-4 py-3 rounded-2xl text-sm leading-relaxed ${
          isUser
            ? 'bg-primary-600/25 text-white border border-primary-500/30 rounded-tr-sm'
            : 'glass text-slate-200 border border-white/10 rounded-tl-sm'
        }`}>
          {renderContent()}
        </div>

        {/* Fallacy badges */}
        {message.hasFallacy && message.fallacies && message.fallacies.length > 0 && (
          <div className="flex flex-wrap gap-1 mt-1.5">
            {message.fallacies.map((f, i) => (
              <button key={i} onClick={() => onFallacyClick(f)}
                className="flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-semibold transition-all hover:scale-105"
                style={{ background: `${f.color}20`, border: `1px solid ${f.color}40`, color: f.color }}>
                <AlertTriangle className="w-2.5 h-2.5" />
                {f.name}
              </button>
            ))}
          </div>
        )}

        {/* Scores */}
        {isUser && message.confidenceScore !== undefined && (
          <div className="flex items-center gap-3 mt-1.5 text-xs text-slate-500">
            <span>Logic: <span className="text-primary-400 font-semibold">{message.logicScore}%</span></span>
            <span>Confidence: <span className="text-indigo-400 font-semibold">{message.confidenceScore}%</span></span>
          </div>
        )}

        <div className="text-xs text-slate-600 mt-1">
          {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>
    </motion.div>
  )
}

export default function DebatePage() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const { user } = useAuthStore()
  const { currentDebate, messages, isTyping, isLoading, setCurrentDebate, addMessage, setMessages, setTyping, setLoading, clearDebate } = useDebateStore()

  const [setupMode, setSetupMode] = useState(!currentDebate)
  const [topic, setTopic] = useState(searchParams.get('topic') || '')
  const [difficulty, setDifficulty] = useState<string>(user?.difficultyLevel || 'intermediate')
  const [aiPersonality, setAiPersonality] = useState('logical')
  const [userPosition, setUserPosition] = useState('')
  const [inputText, setInputText] = useState('')
  const [isPaused, setIsPaused] = useState(false)
  const [activeFallacy, setActiveFallacy] = useState<Fallacy | null>(null)
  const [showSummary, setShowSummary] = useState(false)
  const [summary, setSummary] = useState<any>(null)
  const [turnCount, setTurnCount] = useState(0)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isTyping])

  const startDebate = async () => {
    if (!topic.trim()) return toast.error('Please enter a debate topic')
    setLoading(true)
    try {
      const data = await debateService.startDebate({ topic, difficulty, aiPersonality, userPosition })
      setCurrentDebate(data.debate)
      setMessages([{
        id: data.openingMessage.id,
        sender: 'ai',
        content: data.openingMessage.content,
        timestamp: data.openingMessage.timestamp,
      }])
      setSetupMode(false)
      setTurnCount(1)
      toast.success('Debate started! Respond to Aria\'s opening.')
    } catch (err: any) {
      toast.error(err.response?.data?.error || 'Failed to start debate')
    } finally {
      setLoading(false)
    }
  }

  const sendMessage = async () => {
    if (!inputText.trim() || !currentDebate || isPaused) return
    const content = inputText.trim()
    setInputText('')
    setTyping(true)

    const tempId = `temp-${Date.now()}`
    const tempUserMsg: DebateMessage = {
      id: tempId,
      sender: 'user',
      content,
      timestamp: new Date().toISOString(),
    }
    addMessage(tempUserMsg)

    try {
      const data = await debateService.sendMessage(currentDebate.id, content)
      // Use store's setState directly to avoid stale closure
      const { messages: currentMessages } = useDebateStore.getState()
      setMessages([
        ...currentMessages.filter(m => m.id !== tempId),
        data.userMessage,
        data.aiMessage,
      ])
      setTurnCount(t => t + 1)
    } catch (err: any) {
      toast.error(err.response?.data?.error || 'Failed to send message')
      const { messages: currentMessages } = useDebateStore.getState()
      setMessages(currentMessages.filter(m => m.id !== tempId))
    } finally {
      setTyping(false)
    }
  }

  const endDebate = async () => {
    if (!currentDebate) return
    setLoading(true)
    try {
      const data = await debateService.endDebate(currentDebate.id)
      setSummary(data.summary)
      setShowSummary(true)
    } catch (err: any) {
      toast.error('Failed to end debate')
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  if (showSummary && summary) {
    return (
      <div className="min-h-screen bg-dark flex items-center justify-center relative overflow-hidden px-4">
        <GradientOrbs />
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="relative z-10 w-full max-w-2xl glass-card p-8 rounded-3xl border border-white/10"
        >
          <div className="text-center mb-8">
            <div className="text-5xl mb-4">{summary.winner === 'user' ? '🏆' : summary.winner === 'draw' ? '🤝' : '📚'}</div>
            <h2 className="text-3xl font-display font-black text-white mb-2">Debate Complete!</h2>
            <p className="text-slate-400">{summary.topic}</p>
          </div>

          <div className="grid grid-cols-3 gap-4 mb-6">
            {[
              { label: 'Final Score', value: `${summary.finalScore}%`, color: '#2563EB' },
              { label: 'Logic Score', value: `${summary.logicScore}%`, color: '#10B981' },
              { label: 'XP Earned', value: `+${summary.xpEarned}`, color: '#F59E0B' },
            ].map(({ label, value, color }) => (
              <div key={label} className="glass rounded-xl p-4 text-center border border-white/10">
                <div className="text-2xl font-black mb-1" style={{ color }}>{value}</div>
                <div className="text-xs text-slate-500">{label}</div>
              </div>
            ))}
          </div>

          {summary.summary && (
            <div className="glass rounded-xl p-4 mb-4 border border-white/10">
              <p className="text-slate-300 text-sm leading-relaxed">{summary.summary}</p>
            </div>
          )}

          {summary.keyInsights?.length > 0 && (
            <div className="mb-4">
              <h4 className="text-white font-semibold text-sm mb-2">Key Insights</h4>
              <ul className="space-y-1">
                {summary.keyInsights.map((insight: string, i: number) => (
                  <li key={i} className="text-slate-400 text-xs flex items-start gap-2">
                    <span className="text-primary-400 mt-0.5">•</span>{insight}
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div className="flex gap-3">
            <button onClick={() => { clearDebate(); setSetupMode(true); setShowSummary(false); setSummary(null) }}
              className="flex-1 py-3 bg-primary-600 hover:bg-primary-500 text-white font-bold rounded-xl transition-all">
              New Debate
            </button>
            <button onClick={() => navigate('/dashboard')}
              className="flex-1 py-3 glass hover:bg-white/10 text-white font-bold rounded-xl transition-all border border-white/10">
              Dashboard
            </button>
          </div>
        </motion.div>
      </div>
    )
  }

  if (setupMode) {
    return (
      <div className="min-h-screen bg-dark flex items-center justify-center relative overflow-hidden px-4 py-12">
        <GradientOrbs />
        <div className="absolute inset-0 bg-grid opacity-20" />
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          className="relative z-10 w-full max-w-2xl"
        >
          <div className="text-center mb-8">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary-600 to-indigo-500 flex items-center justify-center mx-auto mb-4 shadow-glow-blue">
              <Brain className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-3xl font-display font-black text-white mb-2">Start a Debate</h1>
            <p className="text-slate-400">Configure your debate session with Aria</p>
          </div>

          <div className="glass-card p-8 rounded-3xl border border-white/10 space-y-6">
            {/* Topic */}
            <div>
              <label className="block text-sm font-semibold text-slate-300 mb-2">Debate Topic *</label>
              <textarea value={topic} onChange={(e) => setTopic(e.target.value)}
                placeholder="e.g., Social media does more harm than good"
                className="w-full h-20 bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-slate-600 text-sm resize-none outline-none focus:border-primary-500/50 transition-all"
              />
            </div>

            {/* Your Position */}
            <div>
              <label className="block text-sm font-semibold text-slate-300 mb-2">Your Position (optional)</label>
              <input value={userPosition} onChange={(e) => setUserPosition(e.target.value)}
                placeholder="e.g., I argue that social media is harmful..."
                className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-slate-600 text-sm outline-none focus:border-primary-500/50 transition-all"
              />
            </div>

            {/* Difficulty */}
            <div>
              <label className="block text-sm font-semibold text-slate-300 mb-3">Difficulty Level</label>
              <div className="grid grid-cols-4 gap-2">
                {['beginner', 'intermediate', 'advanced', 'expert'].map((d) => (
                  <button key={d} onClick={() => setDifficulty(d)}
                    className={`py-2 px-3 rounded-xl text-xs font-semibold capitalize transition-all border ${
                      difficulty === d ? 'border-primary-500/50 bg-primary-600/20 text-white' : 'border-white/10 text-slate-400 hover:text-white hover:bg-white/5'
                    }`}
                    style={difficulty === d ? { color: DIFFICULTY_COLORS[d as keyof typeof DIFFICULTY_COLORS] } : {}}>
                    {d}
                  </button>
                ))}
              </div>
            </div>

            {/* AI Personality */}
            <div>
              <label className="block text-sm font-semibold text-slate-300 mb-3">AI Personality</label>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {AI_PERSONALITIES.map((p) => (
                  <button key={p.id} onClick={() => setAiPersonality(p.id)}
                    className={`flex items-center gap-3 p-3 rounded-xl border text-left transition-all ${
                      aiPersonality === p.id ? 'border-primary-500/50 bg-primary-600/20' : 'border-white/10 hover:bg-white/5'
                    }`}>
                    <span className="text-xl">{p.icon}</span>
                    <div>
                      <div className="text-white text-sm font-semibold">{p.name}</div>
                      <div className="text-slate-500 text-xs">{p.description}</div>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            <button onClick={startDebate} disabled={isLoading || !topic.trim()}
              className="w-full flex items-center justify-center gap-3 py-4 bg-primary-600 hover:bg-primary-500 disabled:opacity-50 text-white font-bold rounded-xl transition-all shadow-glow-blue hover:shadow-glow-indigo text-lg">
              {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : <><Brain className="w-5 h-5" />Begin Debate</>}
            </button>
          </div>
        </motion.div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-dark flex flex-col relative overflow-hidden">
      <GradientOrbs />
      <div className="absolute inset-0 bg-grid opacity-10 pointer-events-none" />

      {/* Header */}
      <div className="relative z-10 glass-dark border-b border-white/10 px-4 py-3 pt-16">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button onClick={() => navigate('/dashboard')} className="text-slate-400 hover:text-white transition-colors">
              <ArrowLeft className="w-5 h-5" />
            </button>
            <div>
              <div className="text-white font-semibold text-sm truncate max-w-xs">{currentDebate?.topic}</div>
              <div className="flex items-center gap-2 text-xs text-slate-500">
                <span className="capitalize" style={{ color: DIFFICULTY_COLORS[currentDebate?.difficulty as keyof typeof DIFFICULTY_COLORS] || '#94A3B8' }}>
                  {currentDebate?.difficulty}
                </span>
                <span>·</span>
                <span>Turn {turnCount}</span>
                <span>·</span>
                <div className={`w-1.5 h-1.5 rounded-full ${isPaused ? 'bg-warning' : 'bg-success'} animate-pulse`} />
                <span>{isPaused ? 'Paused' : 'Live'}</span>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button onClick={() => setIsPaused(!isPaused)}
              className="glass p-2 rounded-lg text-slate-400 hover:text-white transition-all border border-white/10">
              {isPaused ? <Play className="w-4 h-4" /> : <Pause className="w-4 h-4" />}
            </button>
            <button onClick={endDebate} disabled={isLoading}
              className="flex items-center gap-1.5 px-3 py-2 bg-error/20 hover:bg-error/30 text-error rounded-lg text-xs font-semibold transition-all border border-error/30">
              {isLoading ? <Loader2 className="w-3 h-3 animate-spin" /> : <Square className="w-3 h-3" />}
              End
            </button>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="relative z-10 flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-4xl mx-auto">
          {messages.length === 0 && (
            <div className="text-center py-20 text-slate-600">
              <MessageSquare className="w-12 h-12 mx-auto mb-3 opacity-30" />
              <p>Starting debate...</p>
            </div>
          )}
          {messages.map((msg) => (
            <MessageBubble key={msg.id} message={msg} onFallacyClick={setActiveFallacy} />
          ))}
          {isTyping && (
            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="flex justify-start mb-4">
              <div className="flex items-center gap-2 mb-1.5">
                <div className="w-6 h-6 rounded-full bg-gradient-to-br from-primary-600 to-indigo-500 flex items-center justify-center">
                  <Brain className="w-3 h-3 text-white" />
                </div>
              </div>
              <div className="glass rounded-2xl rounded-tl-sm border border-white/10 px-4 py-3 ml-2">
                <div className="flex gap-1">
                  {[0, 1, 2].map((i) => (
                    <div key={i} className="typing-dot" style={{ animationDelay: `${i * 0.2}s` }} />
                  ))}
                </div>
              </div>
            </motion.div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Fallacy Panel */}
      <AnimatePresence>
        {activeFallacy && (
          <motion.div
            initial={{ opacity: 0, x: 300 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 300 }}
            className="fixed right-4 top-1/2 -translate-y-1/2 z-50 w-72 glass-dark rounded-2xl p-5 border shadow-glass"
            style={{ borderColor: `${activeFallacy.color}40` }}
          >
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <AlertTriangle className="w-4 h-4" style={{ color: activeFallacy.color }} />
                <span className="font-bold text-sm" style={{ color: activeFallacy.color }}>{activeFallacy.name}</span>
              </div>
              <button onClick={() => setActiveFallacy(null)} className="text-slate-500 hover:text-white text-sm">✕</button>
            </div>
            <p className="text-slate-300 text-xs leading-relaxed mb-3">{activeFallacy.description}</p>
            <div className="flex items-center gap-2 text-xs">
              <span className="text-slate-500">Confidence:</span>
              <div className="flex-1 h-1.5 bg-white/10 rounded-full overflow-hidden">
                <div className="h-full rounded-full" style={{ width: `${Math.round(activeFallacy.confidence * 100)}%`, background: activeFallacy.color }} />
              </div>
              <span className="font-bold" style={{ color: activeFallacy.color }}>{Math.round(activeFallacy.confidence * 100)}%</span>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Input */}
      <div className="relative z-10 glass-dark border-t border-white/10 px-4 py-4">
        <div className="max-w-4xl mx-auto">
          {isPaused && (
            <div className="text-center text-warning text-sm mb-3 flex items-center justify-center gap-2">
              <Pause className="w-4 h-4" /> Debate paused — click play to resume
            </div>
          )}
          <div className="flex items-end gap-3">
            <div className="flex-1 relative">
              <textarea
                ref={inputRef}
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder={isPaused ? 'Debate is paused...' : 'Type your argument... (Enter to send, Shift+Enter for new line)'}
                disabled={isPaused || isTyping}
                rows={2}
                className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-slate-600 text-sm resize-none outline-none focus:border-primary-500/50 transition-all disabled:opacity-50"
              />
              <div className="absolute bottom-2 right-3 text-xs text-slate-600">{inputText.length}/1000</div>
            </div>
            <div className="flex flex-col gap-2">
              <button
                onClick={sendMessage}
                disabled={!inputText.trim() || isPaused || isTyping}
                className="w-11 h-11 bg-primary-600 hover:bg-primary-500 disabled:opacity-40 rounded-xl flex items-center justify-center transition-all shadow-glow-sm"
              >
                {isTyping ? <Loader2 className="w-4 h-4 text-white animate-spin" /> : <Send className="w-4 h-4 text-white" />}
              </button>
            </div>
          </div>
          <div className="flex items-center justify-between mt-2 text-xs text-slate-600">
            <span>Fallacies detected this session: <span className="text-warning font-semibold">{messages.filter(m => m.hasFallacy).length}</span></span>
            <span className="flex items-center gap-1"><Zap className="w-3 h-3 text-warning" /> Powered by Gemini 2.5</span>
          </div>
        </div>
      </div>
    </div>
  )
}
