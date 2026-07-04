from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FileRecord(BaseModel):
    id:Optional[int]=None
    filename:str
    path:str
    size:int
    content_type:Optional[str]=None
    skill:Optional[str]=None
    uploaded_at:Optional[datetime]=None