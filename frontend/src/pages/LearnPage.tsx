import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useQuery } from '@tanstack/react-query'
import { BookOpen, Search, AlertTriangle, CheckCircle, Brain, Zap, ChevronRight, X, Star } from 'lucide-react'
import { fallacyService } from '../services/fallacy.service'
import GradientOrbs from '../components/animations/GradientOrbs'
import SectionReveal from '../components/common/SectionReveal'
import type { FallacyLibraryItem } from '../types'

const QUIZ_QUESTIONS = [
  { id: 1, question: 'Which fallacy involves attacking the person rather than their argument?', options: ['Straw Man', 'Ad Hominem', 'Slippery Slope', 'Bandwagon'], correct: 1, explanation: 'Ad Hominem attacks the person making the argument rather than addressing the argument itself.' },
  { id: 2, question: 'What is a "False Dilemma"?', options: ['Presenting only two options when more exist', 'Using emotions to persuade', 'Generalizing from few examples', 'Attacking the person'], correct: 0, explanation: 'A False Dilemma presents only two choices when in reality more options exist.' },
  { id: 3, question: 'Which fallacy assumes one event will lead to extreme consequences?', options: ['Bandwagon', 'Ad Hominem', 'Slippery Slope', 'Red Herring'], correct: 2, explanation: 'The Slippery Slope fallacy assumes that one event will inevitably lead to extreme consequences without evidence.' },
  { id: 4, question: '"Everyone is doing it, so it must be right" is an example of:', options: ['Appeal to Authority', 'Bandwagon', 'Hasty Generalization', 'Circular Reasoning'], correct: 1, explanation: 'The Bandwagon fallacy argues something is true or good because many people believe or do it.' },
  { id: 5, question: 'Drawing broad conclusions from a small sample is called:', options: ['False Dilemma', 'Straw Man', 'Hasty Generalization', 'Appeal to Emotion'], correct: 2, explanation: 'Hasty Generalization involves drawing broad conclusions from insufficient or unrepresentative evidence.' },
]

const FLASHCARDS = [
  { front: 'Ad Hominem', back: 'Attacking the person making the argument rather than the argument itself.', color: '#EF4444', icon: '👤' },
  { front: 'Straw Man', back: 'Misrepresenting someone\'s argument to make it easier to attack.', color: '#F59E0B', icon: '🎭' },
  { front: 'Slippery Slope', back: 'Assuming one event will inevitably lead to extreme consequences without justification.', color: '#8B5CF6', icon: '📉' },
  { front: 'Appeal to Emotion', back: 'Manipulating emotions rather than using logical reasoning to support a claim.', color: '#EC4899', icon: '💔' },
  { front: 'False Dilemma', back: 'Presenting only two options when more alternatives exist.', color: '#06B6D4', icon: '⚖️' },
  { front: 'Bandwagon', back: 'Arguing something is true or good because many people believe it.', color: '#10B981', icon: '🚂' },
]

function FlashCard({ card }: { card: typeof FLASHCARDS[0] }) {
  const [flipped, setFlipped] = useState(false)
  return (
    <div className="perspective-1000 h-40 cursor-pointer" onClick={() => setFlipped(!flipped)}>
      <motion.div
        animate={{ rotateY: flipped ? 180 : 0 }}
        transition={{ duration: 0.5 }}
        className="relative w-full h-full transform-style-3d"
      >
        {/* Front */}
        <div className="absolute inset-0 backface-hidden glass-card rounded-2xl flex flex-col items-center justify-center p-4 border border-white/10"
          style={{ borderColor: `${card.color}30` }}>
          <div className="text-3xl mb-2">{card.icon}</div>
          <div className="text-white font-bold text-center">{card.front}</div>
          <div className="text-xs text-slate-500 mt-2">Click to reveal</div>
        </div>
        {/* Back */}
        <div className="absolute inset-0 backface-hidden glass-card rounded-2xl flex items-center justify-center p-4 border"
          style={{ transform: 'rotateY(180deg)', borderColor: `${card.color}40`, background: `${card.color}10` }}>
          <p className="text-slate-200 text-sm text-center leading-relaxed">{card.back}</p>
        </div>
      </motion.div>
    </div>
  )
}

function QuizSection() {
  const [currentQ, setCurrentQ] = useState(0)
  const [selected, setSelected] = useState<number | null>(null)
  const [score, setScore] = useState(0)
  const [completed, setCompleted] = useState(false)
  const [showExplanation, setShowExplanation] = useState(false)

  const q = QUIZ_QUESTIONS[currentQ]

  const handleAnswer = (idx: number) => {
    if (selected !== null) return
    setSelected(idx)
    setShowExplanation(true)
    if (idx === q.correct) setScore(s => s + 1)
  }

  const next = () => {
    if (currentQ < QUIZ_QUESTIONS.length - 1) {
      setCurrentQ(c => c + 1)
      setSelected(null)
      setShowExplanation(false)
    } else {
      setCompleted(true)
    }
  }

  const reset = () => { setCurrentQ(0); setSelected(null); setScore(0); setCompleted(false); setShowExplanation(false) }

  if (completed) {
    return (
      <div className="text-center py-8">
        <div className="text-5xl mb-4">{score >= 4 ? '🏆' : score >= 3 ? '🎯' : '📚'}</div>
        <h3 className="text-2xl font-bold text-white mb-2">Quiz Complete!</h3>
        <p className="text-slate-400 mb-2">You scored <span className="text-primary-400 font-bold">{score}/{QUIZ_QUESTIONS.length}</span></p>
        <p className="text-slate-500 text-sm mb-6">{score >= 4 ? 'Excellent! You have a strong grasp of logical fallacies.' : 'Keep practicing to improve your fallacy detection skills.'}</p>
        <button onClick={reset} className="px-6 py-3 bg-primary-600 hover:bg-primary-500 text-white font-bold rounded-xl transition-all">
          Try Again
        </button>
      </div>
    )
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <span className="text-slate-400 text-sm">Question {currentQ + 1} of {QUIZ_QUESTIONS.length}</span>
        <span className="text-primary-400 font-semibold text-sm">Score: {score}</span>
      </div>
      <div className="score-bar mb-6">
        <div className="score-fill" style={{ width: `${((currentQ) / QUIZ_QUESTIONS.length) * 100}%` }} />
      </div>
      <h3 className="text-white font-bold text-lg mb-6">{q.question}</h3>
      <div className="space-y-3 mb-6">
        {q.options.map((opt, i) => (
          <button key={i} onClick={() => handleAnswer(i)}
            className={`w-full text-left px-4 py-3 rounded-xl border text-sm font-medium transition-all ${
              selected === null ? 'border-white/10 text-slate-300 hover:border-primary-500/50 hover:bg-primary-600/10' :
              i === q.correct ? 'border-success/50 bg-success/10 text-success' :
              i === selected ? 'border-error/50 bg-error/10 text-error' :
              'border-white/5 text-slate-500'
            }`}>
            <span className="mr-3 font-bold">{String.fromCharCode(65 + i)}.</span>{opt}
          </button>
        ))}
      </div>
      <AnimatePresence>
        {showExplanation && (
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
            className={`p-4 rounded-xl border mb-4 text-sm ${selected === q.correct ? 'bg-success/10 border-success/30 text-success' : 'bg-error/10 border-error/30 text-error'}`}>
            <div className="flex items-center gap-2 mb-1 font-semibold">
              {selected === q.correct ? <CheckCircle className="w-4 h-4" /> : <X className="w-4 h-4" />}
              {selected === q.correct ? 'Correct!' : 'Incorrect'}
            </div>
            <p className="text-slate-300 text-xs">{q.explanation}</p>
          </motion.div>
        )}
      </AnimatePresence>
      {selected !== null && (
        <button onClick={next} className="w-full py-3 bg-primary-600 hover:bg-primary-500 text-white font-bold rounded-xl transition-all flex items-center justify-center gap-2">
          {currentQ < QUIZ_QUESTIONS.length - 1 ? 'Next Question' : 'See Results'}
          <ChevronRight className="w-4 h-4" />
        </button>
      )}
    </div>
  )
}

export default function LearnPage() {
  const [activeTab, setActiveTab] = useState<'library' | 'flashcards' | 'quiz'>('library')
  const [search, setSearch] = useState('')
  const [selectedFallacy, setSelectedFallacy] = useState<FallacyLibraryItem | null>(null)

  const { data: libraryData } = useQuery({
    queryKey: ['fallacy-library'],
    queryFn: fallacyService.getLibrary,
  })

  const fallacies: FallacyLibraryItem[] = libraryData?.fallacies || []
  const filtered = fallacies.filter(f =>
    f.name.toLowerCase().includes(search.toLowerCase()) ||
    f.description.toLowerCase().includes(search.toLowerCase())
  )

  const TABS = [
    { id: 'library', label: 'Fallacy Library', icon: BookOpen },
    { id: 'flashcards', label: 'Flashcards', icon: Star },
    { id: 'quiz', label: 'Quiz', icon: Brain },
  ]

  return (
    <div className="min-h-screen bg-dark relative overflow-hidden">
      <GradientOrbs />
      <div className="absolute inset-0 bg-grid opacity-20 pointer-events-none" />

      <div className="relative z-10 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pt-24">
        <SectionReveal className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-600 to-indigo-500 flex items-center justify-center">
              <BookOpen className="w-5 h-5 text-white" />
            </div>
            <h1 className="text-3xl font-display font-black text-white">Learning Hub</h1>
          </div>
          <p className="text-slate-400">Master logical fallacies, sharpen your reasoning, and become a better debater.</p>
        </SectionReveal>

        {/* Tabs */}
        <div className="flex gap-2 mb-8 glass-card p-1 rounded-2xl border border-white/10 w-fit">
          {TABS.map(({ id, label, icon: Icon }) => (
            <button key={id} onClick={() => setActiveTab(id as any)}
              className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold transition-all ${
                activeTab === id ? 'bg-primary-600 text-white shadow-glow-sm' : 'text-slate-400 hover:text-white'
              }`}>
              <Icon className="w-4 h-4" />
              {label}
            </button>
          ))}
        </div>

        {/* Library Tab */}
        {activeTab === 'library' && (
          <div>
            <div className="relative mb-6">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
              <input value={search} onChange={(e) => setSearch(e.target.value)}
                placeholder="Search fallacies..."
                className="w-full max-w-md bg-white/5 border border-white/10 rounded-xl pl-11 pr-4 py-3 text-white placeholder-slate-600 text-sm outline-none focus:border-primary-500/50 transition-all"
              />
            </div>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {filtered.map((fallacy, i) => (
                <motion.div key={fallacy.type}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.05 }}
                  onClick={() => setSelectedFallacy(fallacy)}
                  className="glass-card p-5 rounded-2xl border border-white/10 cursor-pointer card-hover"
                  style={{ borderColor: selectedFallacy?.type === fallacy.type ? `${fallacy.color}50` : undefined }}
                >
                  <div className="flex items-center gap-3 mb-3">
                    <div className="w-10 h-10 rounded-xl flex items-center justify-center text-xl"
                      style={{ background: `${fallacy.color}20` }}>
                      {fallacy.icon}
                    </div>
                    <div>
                      <h3 className="text-white font-bold text-sm">{fallacy.name}</h3>
                      <span className="text-xs px-2 py-0.5 rounded-full capitalize"
                        style={{ background: `${fallacy.color}15`, color: fallacy.color }}>
                        {fallacy.category}
                      </span>
                    </div>
                  </div>
                  <p className="text-slate-400 text-xs leading-relaxed">{fallacy.shortDescription}</p>
                </motion.div>
              ))}
            </div>
          </div>
        )}

        {/* Flashcards Tab */}
        {activeTab === 'flashcards' && (
          <div>
            <p className="text-slate-400 text-sm mb-6">Click each card to reveal the definition.</p>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {FLASHCARDS.map((card, i) => (
                <motion.div key={card.front} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.08 }}>
                  <FlashCard card={card} />
                </motion.div>
              ))}
            </div>
          </div>
        )}

        {/* Quiz Tab */}
        {activeTab === 'quiz' && (
          <div className="max-w-2xl mx-auto">
            <div className="glass-card p-8 rounded-3xl border border-white/10">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-xl bg-primary-600/20 flex items-center justify-center">
                  <Brain className="w-5 h-5 text-primary-400" />
                </div>
                <div>
                  <h2 className="text-white font-bold">Fallacy Identification Quiz</h2>
                  <p className="text-slate-500 text-xs">Test your knowledge of logical fallacies</p>
                </div>
              </div>
              <QuizSection />
            </div>
          </div>
        )}
      </div>

      {/* Fallacy Detail Modal */}
      <AnimatePresence>
        {selectedFallacy && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
            onClick={() => setSelectedFallacy(null)}
          >
            <motion.div
              initial={{ scale: 0.9, y: 20 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.9, y: 20 }}
              onClick={(e) => e.stopPropagation()}
              className="w-full max-w-lg glass-dark rounded-3xl p-8 border shadow-glass"
              style={{ borderColor: `${selectedFallacy.color}40` }}
            >
              <div className="flex items-start justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-xl flex items-center justify-center text-2xl"
                    style={{ background: `${selectedFallacy.color}20` }}>
                    {selectedFallacy.icon}
                  </div>
                  <div>
                    <h2 className="text-white font-black text-xl">{selectedFallacy.name}</h2>
                    <span className="text-xs px-2 py-0.5 rounded-full capitalize"
                      style={{ background: `${selectedFallacy.color}20`, color: selectedFallacy.color }}>
                      {selectedFallacy.category}
                    </span>
                  </div>
                </div>
                <button onClick={() => setSelectedFallacy(null)} className="text-slate-500 hover:text-white transition-colors">
                  <X className="w-5 h-5" />
                </button>
              </div>

              <p className="text-slate-300 leading-relaxed mb-6">{selectedFallacy.description}</p>

              <div className="space-y-4">
                <div>
                  <div className="flex items-center gap-2 text-xs text-error font-semibold mb-2">
                    <AlertTriangle className="w-3 h-3" /> Fallacious Example
                  </div>
                  <p className="text-slate-300 text-sm italic bg-error/10 border border-error/20 rounded-xl p-4">
                    {selectedFallacy.example}
                  </p>
                </div>
                <div>
                  <div className="flex items-center gap-2 text-xs text-success font-semibold mb-2">
                    <CheckCircle className="w-3 h-3" /> Corrected Version
                  </div>
                  <p className="text-slate-300 text-sm italic bg-success/10 border border-success/20 rounded-xl p-4">
                    {selectedFallacy.correctedExample}
                  </p>
                </div>
                {selectedFallacy.tips && (
                  <div>
                    <div className="flex items-center gap-2 text-xs text-primary-400 font-semibold mb-2">
                      <Zap className="w-3 h-3" /> Tips to Avoid
                    </div>
                    <ul className="space-y-1">
                      {selectedFallacy.tips.map((tip, i) => (
                        <li key={i} className="text-slate-400 text-xs flex items-start gap-2">
                          <span className="text-primary-400 mt-0.5">•</span>{tip}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
