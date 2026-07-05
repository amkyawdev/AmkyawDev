from pydantic import BaseModel, Field
from typing import Optional
class FileExportRequest(BaseModel):
    format:str=Field("zip",pattern="^(zip|pdf)$")
    skill:Optional[str]=Field(None,description="Filter by skill")
    file_paths:Optional[list[str]]=Field(None,description="Specific files to export")
class FileUploadResponse(BaseModel):
    filename:str
    path:str
    size:int
    content_type:str
class FileInfo(BaseModel):
    name:str
    path:str
    size:int
    modified:str
    skill:Optional[str]=None
