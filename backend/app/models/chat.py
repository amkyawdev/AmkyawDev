from pydantic import BaseModel, Field
from typing import Optional
class ChatMessage(BaseModel):
    role:str=Field(...,pattern="^(system|user|assistant)$")
    content:str=Field(...,min_length=1)
class ChatRequest(BaseModel):
    messages:list[ChatMessage]=Field(...,min_length=1)
    skills:Optional[list[str]]=Field(None,description="Skill names to load")
    model:Optional[str]=Field(None,description="LLM model to use")
    stream:bool=Field(False,description="Enable streaming response")
class ChatResponse(BaseModel):
    message:str
    skills_used:list[str]=[]
    tokens_used:int=0
