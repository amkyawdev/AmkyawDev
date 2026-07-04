from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.routes.agent import router as agent_router
from app.api.routes.knowledge import router as knowledge_router
from app.api.routes.files import router as files_router
from app.api.routes.telegram import router as telegram_router
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 AI Brain Coder Agent starting up...")
    yield
    logger.info("👋 AI Brain Coder Agent shutting down...")


app = FastAPI(
    title="AI Brain Coder Agent",
    description="AI-powered coding assistant with dynamic skill loading",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent_router, prefix="/api/agent", tags=["Agent"])
app.include_router(knowledge_router, prefix="/api/knowledge", tags=["Knowledge"])
app.include_router(files_router, prefix="/api/files", tags=["Files"])
app.include_router(telegram_router, prefix="/api/telegram", tags=["Telegram"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ai-brain-coder-agent"}
