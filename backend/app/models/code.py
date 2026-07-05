from pydantic import BaseModel, Field
from typing import Optional
class CodeGenerationRequest(BaseModel):
    prompt:str=Field(...,min_length=1,description="What code to generate")
    language:str=Field("python",description="Target programming language")
    skills:Optional[list[str]]=Field(None,description="Skills to load")
    context:Optional[str]=Field(None,description="Additional context/codebase info")
    model:Optional[str]=Field(None,description="LLM model override")
class CodeGenerationResponse(BaseModel):
    code:str=Field(...,description="Generated code")
    language:str=Field(...,description="Language of generated code")
    explanation:Optional[str]=Field("",description="Explanation of the approach")
    file_path:Optional[str]=Field(None,description="Where to save the file")
