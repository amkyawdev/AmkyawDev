# AmkyawDev Tools

A full-stack AI-powered coding platform with dynamic skill loading, vector search knowledge base, and multi-modal integration capabilities.

> GitHub: [amkyaw.dev](https://github.com/amkyawdev/ai-brain-skills)

## Architecture

```
amkyawdev-tools/
├── backend/          # Python FastAPI backend
├── frontend/         # Next.js frontend
├── shared/           # Shared types & constants
└── docker-compose.yml
```

## Features

- 🤖 **AI Coder Agent** — AI agent with dynamic `.amkyaw` skill loading
- 🔍 **Knowledge Base** — Vector search via Qdrant for semantic code/document retrieval
- 💬 **Chat Interface** — Real-time AI conversations with syntax-highlighted code blocks
- 📁 **File Manager** — Upload, export (ZIP/PDF), and manage project files
- 📱 **Telegram Bot** — Webhook-based Telegram integration for mobile access
- 🗃️ **PostgreSQL** — Neon serverless Postgres for persistence
- 🎙️ **Text-to-Speech** — ElevenLabs integration for voice output

## Tech Stack

| Layer    | Technology                          |
|----------|-------------------------------------|
| Backend  | FastAPI, Python 3.11+               |
| Frontend | Next.js 14, React, Tailwind CSS     |
| LLM      | OpenRouter (Claude, GPT-4, etc.)    |
| VectorDB | Qdrant                              |
| Database | Neon (Serverless PostgreSQL)        |
| TTS      | ElevenLabs                          |
| NVIDIA   | NVIDIA NIM (optional fallback)      |

## Quick Start

### Prerequisites

- Docker & Docker Compose
- API keys for: OpenRouter, Qdrant, Neon, ElevenLabs (optional)

### Environment Setup

```bash
cp .env.example .env
# Edit .env with your API keys
```

### Run with Docker

```bash
docker-compose up --build
```

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Local Development

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## License

MIT
