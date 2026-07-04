from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.agent import router as agent_router
from app.api.routes.knowledge import router as knowledge_router
from app.utils.logger import setup_logger
logger=setup_logger(__name__)
app=FastAPI(title="AmkyawDev Tools",description="AI-powered coding platform",version="1.0.0")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(agent_router,prefix="/api/agent",tags=["Agent"])
app.include_router(knowledge_router,prefix="/api/knowledge",tags=["Knowledge"])
@app.get("/health")
async def health_check():
    return{"status":"healthy","service":"amkyawdev-tools"}
@app.get("/")
async def root():
    return{"message":"AmkyawDev Tools API","docs":"/docs"}