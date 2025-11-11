# ScholarLens

**Adaptive Scholarship Matching + AI Drafting**

A next-generation scholarship assistance platform that not only matches students to opportunities, but also helps them *apply intelligently* through adaptive, AI-guided essay generation and analysis.

## 🎯 Project Overview

ScholarLens uses AI to learn the hidden "personality" of scholarships and generates tailored application essays aligned to those personalities. It's designed to help students write differentiated, personalized essays for multiple scholarships.

## ✨ Features

- **Persona Builder**: Extracts scholarship personality genome (weights + tone) from descriptions
- **Essay Generator**: Creates personalized essays matching scholarship personas
- **Evaluation Agent**: Compares adaptive vs generic essays with alignment metrics
- **Mirror Test**: Provides improvement suggestions for existing essays
- **Cluster Labeler**: Learns personality patterns from winner essays

## 🏗️ Tech Stack

### Frontend
- React + TypeScript
- Zustand (state management)
- Vite (build tool)
- Recharts (visualization)

### Backend
- FastAPI (Python)
- PostgreSQL
- Anthropic Claude API

## 🚀 Quick Start

### Prerequisites
- Node.js ≥ 18.x
- Python ≥ 3.11
- PostgreSQL ≥ 14
- Anthropic Claude API Key

### Installation

1. Clone the repository:
```bash
git clone git@github.com:Bruce1508/ScholarLens.git
cd ScholarLens
```

2. Set up environment variables:
```bash
cp .env.example .env
# Update CLAUDE_API_KEY and DATABASE_URL in .env
```

3. Install backend dependencies:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Install frontend dependencies:
```bash
cd frontend
npm ci
```

5. Run the application:
```bash
# Backend (from backend/)
uvicorn main:app --reload

# Frontend (from frontend/)
npm run dev
```

## 📚 Documentation

- [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md) - Project overview and architecture
- [DEVELOPEMENT.md](./DEVELOPEMENT.md) - Development setup and guidelines
- [.claude/CLAUDE.md](./.claude/CLAUDE.md) - Claude Code configuration

## 🤝 Contributing

This project is part of the Agentiiv Hackathon Team — AI Innovation Track.

## 📄 License

MIT License - open for educational use and academic collaboration.

## 👥 Team

**Owner:** Nguyen Duc Anh Vo (Bruce Vo)  
**Team:** Agentiiv Hackathon Team — AI Innovation Track

---

**Tagline:** "We don't just help students apply. We help them resonate."

