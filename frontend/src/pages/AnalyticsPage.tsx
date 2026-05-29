import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import { RadarChart, PolarGrid, PolarAngleAxis, Radar, ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, BarChart, Bar, Cell } from 'recharts'
import { BarChart3, TrendingUp, Target, Brain, Trophy, Flame, Zap } from 'lucide-react'
import { analyticsService } from '../services/analytics.service'
import { useAuthStore } from '../store/authStore'
import { TIER_COLORS, TIER_ICONS } from '../constants'
import GradientOrbs from '../components/animations/GradientOrbs'
import SectionReveal from '../components/common/SectionReveal'

const FALLACY_COLORS_MAP: Record<string, string> = {
  ad_hominem: '#EF4444', strawman: '#F59E0B', slippery_slope: '#8B5CF6',
  appeal_to_emotion: '#EC4899', false_dilemma: '#06B6D4', bandwagon: '#10B981',
  hasty_generalization: '#F97316',
}

export default function AnalyticsPage() {
  const { user } = useAuthStore()
  const { data, isLoading } = useQuery({
    queryKey: ['analytics'],
    queryFn: analyticsService.getUserAnalytics,
  })

  const analytics = data?.analytics
  const overview = analytics?.overview
  const skills = analytics?.skills

  const radarData = skills ? [
    { subject: 'Logic', value: skills.logic, fullMark: 100 },
    { subject: 'Persuasion', value: skills.persuasion, fullMark: 100 },
    { subject: 'Evidence', value: skills.evidence, fullMark: 100 },
    { subject: 'Clarity', value: skills.clarity, fullMark: 100 },
    { subject: 'Rebuttal', value: skills.rebuttal, fullMark: 100 },
    { subject: 'Structure', value: skills.structure, fullMark: 100 },
  ] : []

  const logicHistory = analytics?.logicScoreHistory?.slice(-15).map((h: any, i: number) => ({
    day: `D${i + 1}`, score: h.score,
  })) || []

  const fallacyData = analytics?.fallacyBreakdown?.map((f: any) => ({
    name: f.type.replace(/_/g, ' ').replace(/\b\w/g, (c: string) => c.toUpperCase()),
    count: f.count,
    color: FALLACY_COLORS_MAP[f.type] || '#6366F1',
  })) || []

  const tierColor = TIER_COLORS[user?.tier as keyof typeof TIER_COLORS] || '#CD7F32'
  const tierIcon = TIER_ICONS[user?.tier as keyof typeof TIER_ICONS] || '🥉'

  if (isLoading) {
    return (
      <div className="min-h-screen bg-dark flex items-center justify-center">
        <div className="text-center">
          <div className="w-12 h-12 border-2 border-primary-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-slate-400">Loading analytics...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-dark relative overflow-hidden">
      <GradientOrbs />
      <div className="absolute inset-0 bg-grid opacity-20 pointer-events-none" />

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pt-24">
        <SectionReveal className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-600 to-indigo-500 flex items-center justify-center">
              <BarChart3 className="w-5 h-5 text-white" />
            </div>
            <h1 className="text-3xl font-display font-black text-white">Analytics</h1>
          </div>
          <p className="text-slate-400">Track your critical thinking growth and debate performance.</p>
        </SectionReveal>

        {/* Overview Cards */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {[
            { icon: Trophy, label: 'Win Rate', value: `${overview?.winRate || 0}%`, color: '#F59E0B', sub: `${overview?.debatesWon || 0}W / ${overview?.totalDebates || 0}T` },
            { icon: Target, label: 'Logic Score', value: `${overview?.logicScore || 50}`, color: '#10B981', sub: 'Current' },
            { icon: Flame, label: 'Streak', value: `${overview?.streak || user?.streak || 0}`, color: '#EF4444', sub: `Best: ${overview?.longestStreak || 0}` },
            { icon: Zap, label: 'Total XP', value: (overview?.totalXp || user?.xp || 0).toLocaleString(), color: '#F59E0B', sub: `Level ${user?.level}` },
          ].map(({ icon: Icon, label, value, color, sub }, i) => (
            <motion.div key={label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className="glass-card p-5 card-hover"
            >
              <div className="flex items-center justify-between mb-3">
                <div className="w-9 h-9 rounded-lg flex items-center justify-center"
                  style={{ background: `${color}20` }}>
                  <Icon className="w-4 h-4" style={{ color }} />
                </div>
                <span className="text-xs text-slate-500">{sub}</span>
              </div>
              <div className="text-2xl font-black text-white mb-1">{value}</div>
              <div className="text-slate-400 text-xs">{label}</div>
            </motion.div>
          ))}
        </div>

        {/* Tier Badge */}
        <SectionReveal delay={0.2} className="mb-8">
          <div className="glass-card p-6 rounded-2xl border border-white/10 flex items-center gap-6">
            <div className="text-5xl">{tierIcon}</div>
            <div className="flex-1">
              <div className="text-white font-black text-xl mb-1" style={{ color: tierColor }}>{user?.tier} Tier</div>
              <p className="text-slate-400 text-sm">Keep debating to advance to the next tier and unlock exclusive features.</p>
              <div className="mt-3 score-bar">
                <div className="score-fill" style={{ width: `${Math.min(100, ((user?.xp || 0) % 500) / 5)}%`, background: `linear-gradient(90deg, ${tierColor}80, ${tierColor})` }} />
              </div>
            </div>
            <div className="text-right">
              <div className="text-white font-bold">{(user?.xp || 0).toLocaleString()} XP</div>
              <div className="text-slate-500 text-xs">Total earned</div>
            </div>
          </div>
        </SectionReveal>

        {/* Charts Grid */}
        <div className="grid lg:grid-cols-2 gap-6 mb-8">
          {/* Skill Radar */}
          <SectionReveal delay={0.2}>
            <div className="glass-card p-6 rounded-2xl border border-white/10">
              <h3 className="text-white font-bold mb-4 flex items-center gap-2">
                <Brain className="w-4 h-4 text-primary-400" />
                Skill Assessment
              </h3>
              {radarData.length > 0 ? (
                <ResponsiveContainer width="100%" height={280}>
                  <RadarChart data={radarData}>
                    <PolarGrid stroke="rgba(255,255,255,0.08)" />
                    <PolarAngleAxis dataKey="subject" tick={{ fill: '#94A3B8', fontSize: 12 }} />
                    <Radar name="Skills" dataKey="value" stroke="#2563EB" fill="#2563EB" fillOpacity={0.25} strokeWidth={2} dot={{ fill: '#2563EB', r: 4 }} />
                  </RadarChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-[280px] flex items-center justify-center text-slate-500 text-sm">Complete debates to see your skills</div>
              )}
            </div>
          </SectionReveal>

          {/* Logic Score Trend */}
          <SectionReveal delay={0.25}>
            <div className="glass-card p-6 rounded-2xl border border-white/10">
              <h3 className="text-white font-bold mb-4 flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-success" />
                Logic Score Trend
              </h3>
              {logicHistory.length > 0 ? (
                <ResponsiveContainer width="100%" height={280}>
                  <LineChart data={logicHistory}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                    <XAxis dataKey="day" tick={{ fill: '#64748B', fontSize: 11 }} />
                    <YAxis domain={[0, 100]} tick={{ fill: '#64748B', fontSize: 11 }} />
                    <Tooltip contentStyle={{ background: 'rgba(15,23,42,0.95)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', color: '#fff' }} />
                    <Line type="monotone" dataKey="score" stroke="#2563EB" strokeWidth={2.5} dot={{ fill: '#2563EB', r: 4 }} activeDot={{ r: 6, fill: '#6366F1' }} />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-[280px] flex items-center justify-center text-slate-500 text-sm">Complete debates to see your trend</div>
              )}
            </div>
          </SectionReveal>
        </div>

        {/* Fallacy Breakdown */}
        {fallacyData.length > 0 && (
          <SectionReveal delay={0.3} className="mb-8">
            <div className="glass-card p-6 rounded-2xl border border-white/10">
              <h3 className="text-white font-bold mb-4 flex items-center gap-2">
                <Target className="w-4 h-4 text-warning" />
                Fallacy Breakdown
              </h3>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={fallacyData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                  <XAxis dataKey="name" tick={{ fill: '#64748B', fontSize: 10 }} />
                  <YAxis tick={{ fill: '#64748B', fontSize: 11 }} />
                  <Tooltip contentStyle={{ background: 'rgba(15,23,42,0.95)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', color: '#fff' }} />
                  <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                    {fallacyData.map((entry: any, i: number) => (
                      <Cell key={i} fill={entry.color} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </SectionReveal>
        )}

        {/* Recent Debates */}
        {analytics?.recentDebates?.length > 0 && (
          <SectionReveal delay={0.35}>
            <div className="glass-card p-6 rounded-2xl border border-white/10">
              <h3 className="text-white font-bold mb-4">Recent Debates</h3>
              <div className="space-y-3">
                {analytics.recentDebates.map((debate: any) => (
                  <div key={debate._id} className="flex items-center gap-4 p-3 glass rounded-xl border border-white/5">
                    <div className="text-xl">{debate.winner === 'user' ? '🏆' : debate.winner === 'draw' ? '🤝' : '📚'}</div>
                    <div className="flex-1 min-w-0">
                      <div className="text-white text-sm font-medium truncate">{debate.topic}</div>
                      <div className="text-slate-500 text-xs">{new Date(debate.createdAt).toLocaleDateString()} · {debate.totalTurns} turns</div>
                    </div>
                    <div className="text-right">
                      <div className="text-white font-bold">{debate.finalScore || 0}%</div>
                      <div className="text-xs text-success">+{debate.xpEarned || 0} XP</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </SectionReveal>
        )}
      </div>
    </div>
  )
}
