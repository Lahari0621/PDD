import { useState } from 'react'
import { motion } from 'framer-motion'
import { User, Mail, Edit3, Save, X, Trophy, Flame, Zap, MessageSquare, Target, Star } from 'lucide-react'
import { useAuthStore } from '../store/authStore'
import { authService } from '../services/auth.service'
import { TIER_COLORS, TIER_ICONS } from '../constants'
import toast from 'react-hot-toast'
import GradientOrbs from '../components/animations/GradientOrbs'
import SectionReveal from '../components/common/SectionReveal'

const ACHIEVEMENTS = [
  { id: 'first_debate', name: 'First Debate', description: 'Completed your first debate', icon: '🎯', unlocked: true },
  { id: 'fallacy_hunter', name: 'Fallacy Hunter', description: 'Detected 10 fallacies', icon: '🔍', unlocked: true },
  { id: 'streak_7', name: '7-Day Streak', description: 'Debated 7 days in a row', icon: '🔥', unlocked: false },
  { id: 'logic_master', name: 'Logic Master', description: 'Achieved 90%+ logic score', icon: '🧠', unlocked: false },
  { id: 'debate_champion', name: 'Debate Champion', description: 'Won 10 debates', icon: '🏆', unlocked: false },
  { id: 'scholar', name: 'Scholar', description: 'Completed all learning modules', icon: '📚', unlocked: false },
]

export default function ProfilePage() {
  const { user, updateUser } = useAuthStore()
  const [editing, setEditing] = useState(false)
  const [form, setForm] = useState({ username: user?.username || '', bio: user?.bio || '' })
  const [saving, setSaving] = useState(false)

  const tierColor = TIER_COLORS[user?.tier as keyof typeof TIER_COLORS] || '#CD7F32'
  const tierIcon = TIER_ICONS[user?.tier as keyof typeof TIER_ICONS] || '🥉'

  const handleSave = async () => {
    setSaving(true)
    try {
      const data = await authService.updateProfile(form)
      updateUser(data.user)
      setEditing(false)
      toast.success('Profile updated!')
    } catch {
      toast.error('Failed to update profile')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="min-h-screen bg-dark relative overflow-hidden">
      <GradientOrbs />
      <div className="absolute inset-0 bg-grid opacity-20 pointer-events-none" />

      <div className="relative z-10 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pt-24">
        {/* Profile Header */}
        <SectionReveal className="mb-8">
          <div className="glass-card p-8 rounded-3xl border border-white/10">
            <div className="flex flex-col sm:flex-row items-start sm:items-center gap-6">
              {/* Avatar */}
              <div className="relative">
                <div className="w-24 h-24 rounded-3xl bg-gradient-to-br from-primary-600 to-indigo-500 flex items-center justify-center text-4xl font-black text-white shadow-glow-blue">
                  {user?.username?.[0]?.toUpperCase()}
                </div>
                <div className="absolute -bottom-2 -right-2 text-2xl">{tierIcon}</div>
              </div>

              {/* Info */}
              <div className="flex-1">
                {editing ? (
                  <div className="space-y-3">
                    <input value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })}
                      className="bg-white/5 border border-white/10 rounded-xl px-4 py-2 text-white text-lg font-bold outline-none focus:border-primary-500/50 w-full max-w-xs"
                    />
                    <textarea value={form.bio} onChange={(e) => setForm({ ...form, bio: e.target.value })}
                      placeholder="Tell us about yourself..."
                      className="bg-white/5 border border-white/10 rounded-xl px-4 py-2 text-white text-sm outline-none focus:border-primary-500/50 w-full resize-none h-16"
                    />
                    <div className="flex gap-2">
                      <button onClick={handleSave} disabled={saving}
                        className="flex items-center gap-2 px-4 py-2 bg-primary-600 hover:bg-primary-500 text-white text-sm font-semibold rounded-lg transition-all">
                        <Save className="w-3 h-3" /> Save
                      </button>
                      <button onClick={() => setEditing(false)}
                        className="flex items-center gap-2 px-4 py-2 glass text-slate-300 text-sm rounded-lg transition-all border border-white/10">
                        <X className="w-3 h-3" /> Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  <>
                    <div className="flex items-center gap-3 mb-1">
                      <h1 className="text-2xl font-display font-black text-white">{user?.username}</h1>
                      <button onClick={() => setEditing(true)} className="text-slate-500 hover:text-white transition-colors">
                        <Edit3 className="w-4 h-4" />
                      </button>
                    </div>
                    <div className="flex items-center gap-2 text-slate-400 text-sm mb-2">
                      <Mail className="w-3 h-3" />
                      {user?.email}
                    </div>
                    <p className="text-slate-400 text-sm">{user?.bio || 'No bio yet. Click edit to add one.'}</p>
                    <div className="flex items-center gap-4 mt-3">
                      <span className="text-sm font-semibold" style={{ color: tierColor }}>{tierIcon} {user?.tier}</span>
                      <span className="text-slate-500 text-sm">Level {user?.level}</span>
                      <span className="text-slate-500 text-sm capitalize">{user?.plan} plan</span>
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
        </SectionReveal>

        {/* Stats */}
        <SectionReveal delay={0.1} className="mb-8">
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {[
              { icon: MessageSquare, label: 'Debates', value: user?.totalDebates || 0, color: '#2563EB' },
              { icon: Trophy, label: 'Wins', value: user?.debatesWon || 0, color: '#F59E0B' },
              { icon: Target, label: 'Logic Score', value: `${user?.logicScore || 50}`, color: '#10B981' },
              { icon: Flame, label: 'Streak', value: `${user?.streak || 0}d`, color: '#EF4444' },
            ].map(({ icon: Icon, label, value, color }) => (
              <div key={label} className="glass-card p-5 text-center card-hover">
                <div className="w-9 h-9 rounded-lg flex items-center justify-center mx-auto mb-2"
                  style={{ background: `${color}20` }}>
                  <Icon className="w-4 h-4" style={{ color }} />
                </div>
                <div className="text-xl font-black text-white">{value}</div>
                <div className="text-slate-500 text-xs">{label}</div>
              </div>
            ))}
          </div>
        </SectionReveal>

        {/* XP Progress */}
        <SectionReveal delay={0.15} className="mb-8">
          <div className="glass-card p-6 rounded-2xl border border-white/10">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <Zap className="w-4 h-4 text-warning" />
                <span className="text-white font-semibold">Level {user?.level} Progress</span>
              </div>
              <span className="text-warning font-bold">{user?.xp?.toLocaleString()} XP</span>
            </div>
            <div className="score-bar">
              <motion.div
                className="score-fill"
                initial={{ width: 0 }}
                animate={{ width: `${((user?.xp || 0) % 100)}%` }}
                transition={{ duration: 1.5, ease: 'easeOut' }}
              />
            </div>
            <div className="flex justify-between text-xs text-slate-500 mt-1">
              <span>Level {user?.level}</span>
              <span>{100 - ((user?.xp || 0) % 100)} XP to Level {(user?.level || 1) + 1}</span>
            </div>
          </div>
        </SectionReveal>

        {/* Achievements */}
        <SectionReveal delay={0.2}>
          <div className="glass-card p-6 rounded-2xl border border-white/10">
            <h3 className="text-white font-bold mb-4 flex items-center gap-2">
              <Star className="w-4 h-4 text-warning" />
              Achievements
            </h3>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
              {ACHIEVEMENTS.map((achievement, i) => (
                <motion.div
                  key={achievement.id}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: i * 0.05 }}
                  className={`p-4 rounded-xl border text-center transition-all ${
                    achievement.unlocked
                      ? 'border-warning/30 bg-warning/5'
                      : 'border-white/5 opacity-40 grayscale'
                  }`}
                >
                  <div className="text-3xl mb-2">{achievement.icon}</div>
                  <div className="text-white text-xs font-bold mb-1">{achievement.name}</div>
                  <div className="text-slate-500 text-xs">{achievement.description}</div>
                  {achievement.unlocked && (
                    <div className="mt-2 text-xs text-warning font-semibold">Unlocked ✓</div>
                  )}
                </motion.div>
              ))}
            </div>
          </div>
        </SectionReveal>
      </div>
    </div>
  )
}
