from pydantic import BaseModel
from typing import Optional,List

class CodeGenerationRequest(BaseModel):
    prompt:str
    language:Optional[str]=None
    skills:Optional[List[str]]=None

class CodeGenerationResponse(BaseModel):
    code:str
    language:str