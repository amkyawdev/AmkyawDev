from fastapi import APIRouter,Depends,HTTPException
from app.models.chat import ChatRequest,ChatResponse
from app.models.code import CodeGenerationRequest,CodeGenerationResponse
from app.api.dependencies import get_openrouter,get_skill_loader
from app.core.agent import CoderAgent
from app.utils.logger import setup_logger
logger=setup_logger(__name__)
router=APIRouter()
@router.post("/chat",response_model=ChatResponse)
async def chat(request:ChatRequest,openrouter=Depends(get_openrouter),skills_loader=Depends(get_skill_loader)):
    try:
        agent=CoderAgent(openrouter,skills_loader,skills=request.skills)
        reply=await agent.chat(request.messages,request.skills)
        return ChatResponse(message=reply)
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500,detail=str(e))
@router.post("/code",response_model=CodeGenerationResponse)
async def generate_code(request:CodeGenerationRequest,openrouter=Depends(get_openrouter),skills_loader=Depends(get_skill_loader)):
    try:
        agent=CoderAgent(openrouter,skills_loader,skills=request.skills)
        code=await agent.generate_code(request.prompt,request.language,request.skills)
        return CodeGenerationResponse(code=code,language=request.language or"auto")
    except Exception as e:
        logger.error(f"Code generation error: {e}")
        raise HTTPException(status_code=500,detail=str(e))