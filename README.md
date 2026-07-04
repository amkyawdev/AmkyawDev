# AI Brain Coder Agent

Full-stack AI-powered coding assistant with dynamic .amkyaw skill loading, vector search knowledge base, Neon PostgreSQL, and Next.js chat interface.

## Quick Start

```bash
cp .env.example .env
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI, Python 3.11+ |
| Frontend | Next.js 14, React, Tailwind CSS |
| LLM | OpenRouter (Claude, GPT-4) |
| VectorDB | Qdrant |
| Database | Neon (Serverless PostgreSQL) |
| TTS | ElevenLabs |

## License
MIT
