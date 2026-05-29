# 🧠 AI Debate Partner
### *Think Sharper. Argue Better.*

> The future of AI-powered critical thinking training — built with Gemini AI, Hugging Face NLP, React, and Node.js.

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- MongoDB Atlas account
- Gemini API key
- Hugging Face API key

### Backend Setup
```bash
cd backend
npm install
# Edit .env with your credentials
npm run dev
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 🏗️ Architecture

### Frontend (React + Vite + TypeScript)
- **React 18** with TypeScript
- **Tailwind CSS v4** for styling
- **Framer Motion** for animations
- **Zustand** for state management
- **TanStack Query** for data fetching
- **Recharts** for analytics visualizations
- **Socket.io Client** for real-time features

### Backend (Node.js + Express)
- **Express.js** REST API
- **MongoDB Atlas** with Mongoose
- **JWT Authentication** with bcrypt
- **Socket.io** for real-time debate
- **Gemini 1.5 Flash** for AI responses
- **Hugging Face** for NLP fallacy detection

---

## 🤖 AI Pipeline

```
User Argument
     ↓
Rule-Based Detection (regex patterns)
     ↓
Hugging Face NLP (zero-shot classification)
     ↓
Hybrid Fallacy Results
     ↓
Gemini 1.5 Flash (debate response + feedback)
     ↓
Educational Coaching + Analytics
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Create account |
| POST | `/api/auth/login` | Sign in |
| GET | `/api/auth/me` | Get current user |
| POST | `/api/debates/start` | Start debate |
| POST | `/api/debates/message` | Send message |
| POST | `/api/debates/end` | End debate |
| GET | `/api/debates/history` | Debate history |
| POST | `/api/fallacies/analyze` | Analyze text |
| GET | `/api/fallacies/library` | Fallacy library |
| GET | `/api/analytics/user` | User analytics |
| GET | `/api/topics` | Browse topics |

---

## 🔌 Socket Events

| Event | Direction | Description |
|-------|-----------|-------------|
| `join_debate` | Client → Server | Join debate room |
| `send_message` | Client → Server | Send argument |
| `typing` | Client → Server | Typing indicator |
| `ai_response` | Server → Client | AI reply |
| `fallacy_detected` | Server → Client | Fallacy found |
| `typing_started` | Server → Client | AI is typing |
| `debate_summary` | Server → Client | End summary |

---

## 🎨 Design System

| Token | Value |
|-------|-------|
| Primary Blue | `#2563EB` |
| Indigo | `#6366F1` |
| Success | `#10B981` |
| Warning | `#F59E0B` |
| Error | `#EF4444` |
| Dark BG | `#020617` |

---

## 🚢 Deployment

### Frontend → Vercel
```bash
cd frontend
npm run build
# Deploy dist/ to Vercel
```

### Backend → Render/Railway
```bash
# Set environment variables in dashboard
# Deploy from GitHub
```

---

## 🔐 Environment Variables

### Backend `.env`
```
PORT=5000
MONGODB_URI=mongodb+srv://...
JWT_SECRET=your_secret
GEMINI_API_KEY=your_key
HUGGINGFACE_API_KEY=your_key
CLIENT_URL=https://your-frontend.vercel.app
```

### Frontend `.env`
```
VITE_API_URL=https://your-backend.render.com
VITE_SOCKET_URL=https://your-backend.render.com
```

---

## 📊 Features

- ✅ Real-time AI debates with Gemini 1.5 Flash
- ✅ Hybrid fallacy detection (rule-based + Hugging Face)
- ✅ 5 AI personalities (Socratic, Logical, Aggressive, Empathetic, Devil's Advocate)
- ✅ JWT authentication with bcrypt
- ✅ Socket.io real-time communication
- ✅ Analytics dashboard with Recharts
- ✅ Gamification (XP, levels, tiers, streaks, achievements)
- ✅ Learning hub with flashcards and quizzes
- ✅ Responsive design (mobile-first)
- ✅ Cinematic animations with Framer Motion
- ✅ Particle field background
- ✅ Glass morphism UI

---

*Built with ❤️ for critical thinkers everywhere.*
