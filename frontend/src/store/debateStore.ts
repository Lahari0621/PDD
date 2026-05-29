import { create } from 'zustand'
import type { Debate, DebateMessage, Fallacy } from '../types'

interface DebateStore {
  currentDebate: Debate | null
  messages: DebateMessage[]
  isTyping: boolean
  isLoading: boolean
  activeFallacy: Fallacy | null
  isPaused: boolean
  setCurrentDebate: (debate: Debate | null) => void
  addMessage: (message: DebateMessage) => void
  setMessages: (messages: DebateMessage[]) => void
  setTyping: (typing: boolean) => void
  setLoading: (loading: boolean) => void
  setActiveFallacy: (fallacy: Fallacy | null) => void
  setPaused: (paused: boolean) => void
  clearDebate: () => void
}

export const useDebateStore = create<DebateStore>((set) => ({
  currentDebate: null,
  messages: [],
  isTyping: false,
  isLoading: false,
  activeFallacy: null,
  isPaused: false,

  setCurrentDebate: (debate) => set({ currentDebate: debate }),
  addMessage: (message) => set((state) => ({ messages: [...state.messages, message] })),
  setMessages: (messages) => set({ messages }),
  setTyping: (typing) => set({ isTyping: typing }),
  setLoading: (loading) => set({ isLoading: loading }),
  setActiveFallacy: (fallacy) => set({ activeFallacy: fallacy }),
  setPaused: (paused) => set({ isPaused: paused }),
  clearDebate: () => set({ currentDebate: null, messages: [], isTyping: false, activeFallacy: null, isPaused: false }),
}))
