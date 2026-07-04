from pydantic import BaseModel
from typing import Optional,List

class ChatMessage(BaseModel):
    role:str
    content:str

class ChatRequest(BaseModel):
    messages:List[ChatMessage]
    skills:Optional[List[str]]=None

class ChatResponse(BaseModel):
    message:str