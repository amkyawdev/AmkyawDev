# AmkyawDev Tools — AI-Powered Developer Platform

> Full-stack AI agent with dynamic skill injection, vector search (Qdrant),
> text-to-speech (ElevenLabs), and multi-LLM support via OpenRouter.
>
> GitHub: [amkyaw.dev](https://github.com/amkyawdev/tools)

---

## Architecture

```
┌──────────┐       ┌──────────┐
│ Next.js  │◄─────►│ FastAPI  │
│ Frontend │  API  │ Backend  │
└──────────┘       └────┬─────┘
                    │
     ┌──────────────┼──────────────┐
     │              │              │
 ┌───▼───┐  ┌──────▼──────┐  ┌───▼───┐
 │Qdrant │  │  OpenRouter │  │ Neon  │
 │Vector │  │   LLM API   │  │  PG   │
 └───────┘  └─────────────┘  └───────┘
     │
 ┌───▼────┐  ┌──────────┐
 │Eleven  │  │ NVIDIA   │
 │Labs TTS│  │   NIM    │
 └────────┘  └──────────┘
```

## Quick Start

### 1. Clone & Configure

```bash
git clone https://github.com/amkyawdev/tools.git
cd tools
cp .env.example .env
# Edit .env with your API keys
```

### 2. Run with Docker

```bash
docker compose up -d
```

Or manually:

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

## Project Structure

```
tools/
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── api/dependencies.py
│   │   ├── api/routes/agent.py
│   │   ├── api/routes/knowledge.py
│   │   ├── core/agent.py
│   │   ├── core/skill_loader.py
│   │   └── services/
│   │       ├── openrouter_service.py
│   │       ├── qdrant_service.py
│   │       ├── neon_service.py
│   │       ├── elevenlabs_service.py
│   │       └── nvidia_service.py
│   ├── main.py
│   └── requirements.txt
├── frontend/              # Next.js frontend
│   ├── app/
│   ├── components/
│   └── package.json
├── shared/                # Shared types & constants
├── docker-compose.yml
└── README.md
```

## API Endpoints

| Method | Endpoint              | Description               |
|--------|-----------------------|---------------------------|
| GET    | `/health`             | Health check              |
| POST   | `/api/agent/chat`     | Chat with AI agent        |
| POST   | `/api/agent/code`     | Generate code             |
| POST   | `/api/knowledge/search` | Semantic search (Qdrant) |
| GET    | `/api/knowledge/list` | List knowledge entries    |
| POST   | `/api/knowledge/add`  | Add knowledge entry       |
| DELETE | `/api/knowledge/{id}` | Delete knowledge entry    |
| POST   | `/api/files/upload`   | Upload file               |
| POST   | `/api/files/export`   | Export files (ZIP/PDF)    |
| POST   | `/api/files/send-telegram` | Send file via Telegram |
| POST   | `/api/webhook/telegram` | Telegram webhook        |

## Environment Variables

| Variable               | Required | Description                |
|------------------------|----------|----------------------------|
| `OPENROUTER_API_KEY`   | Yes      | OpenRouter API key         |
| `QDRANT_URL`           | Yes      | Qdrant server URL          |
| `QDRANT_API_KEY`       | No       | Qdrant API key (Cloud)     |
| `QDRANT_COLLECTION_NAME`| No      | Collection name (default: amkyawdev-tools) |
| `NEON_DATABASE_URL`    | No       | Neon PostgreSQL URL        |
| `ELEVENLABS_API_KEY`   | No       | ElevenLabs TTS API key     |
| `NVIDIA_API_KEY`       | No       | NVIDIA NIM API key         |
| `TELEGRAM_BOT_TOKEN`   | No       | Telegram bot token         |
| `TELEGRAM_WEBHOOK_SECRET`| No     | Telegram webhook secret    |
| `API_SECRET_KEY`       | No       | API auth secret            |
| `DEBUG`                | No       | Debug mode (default: false)|

## Skills System (`.amkyaw`)

Add `.amkyaw` prompt files to `backend/.amkyaw/`:

```
backend/.amkyaw/
├── python-expert.amkyaw
├── rust-dev.amkyaw
└── web-development.amkyaw
```

The agent loads these dynamically based on the `skills` parameter
in chat/code requests.

## Deploy

### Vercel (Backend)

Connect this repo to Vercel. Config auto-detected from `vercel.json`.
Set environment variables in Vercel dashboard.

### Android APK

Push to `main` branch — GitHub Actions auto-builds APK
(see `.github/workflows/build-android.yml`).
Download from Actions → Artifacts.

## License

MIT — see [LICENSE](LICENSE)
