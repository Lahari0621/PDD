import api from '../api/axios'

export const debateService = {
  startDebate: async (data: {
    topic: string
    topicCategory?: string
    difficulty?: string
    aiPersonality?: string
    userPosition?: string
  }) => {
    const res = await api.post('/debates/start', data)
    return res.data
  },

  sendMessage: async (debateId: string, content: string) => {
    const res = await api.post('/debates/message', { debateId, content })
    return res.data
  },

  endDebate: async (debateId: string) => {
    const res = await api.post('/debates/end', { debateId })
    return res.data
  },

  getHistory: async (page = 1, limit = 10) => {
    const res = await api.get(`/debates/history?page=${page}&limit=${limit}`)
    return res.data
  },

  getDebate: async (id: string) => {
    const res = await api.get(`/debates/${id}`)
    return res.data
  },
}
