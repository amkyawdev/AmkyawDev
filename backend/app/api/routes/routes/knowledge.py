from fastapi import APIRouter,Depends,HTTPException,Query
from pydantic import BaseModel
from typing import Optional
from app.api.dependencies import get_qdrant
from app.utils.logger import setup_logger
logger=setup_logger(__name__)
router=APIRouter()
class KnowledgeEntry(BaseModel):
    title:str
    content:str
    tags:Optional[list[str]]=None
    source:Optional[str]=None
@router.get("/list")
async def list_knowledge(qdrant=Depends(get_qdrant),limit:int=Query(20,ge=1,le=100)):
    try:
        entries=await qdrant.list_all(limit)
        return{"count":len(entries),"entries":entries}
    except Exception as e:
        logger.error(f"List error: {e}")
        return{"count":0,"entries":[]}
@router.post("/search")
async def search_knowledge(query:str=Query(...),qdrant=Depends(get_qdrant),limit:int=Query(10,ge=1,le=50)):
    try:
        results=await qdrant.search(query,limit)
        return{"results":results}
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500,detail=str(e))
@router.post("/add")
async def add_knowledge(entry:KnowledgeEntry,qdrant=Depends(get_qdrant)):
    try:
        entry_id=await qdrant.add(entry.title,entry.content,entry.tags,entry.source)
        return{"id":entry_id,"title":entry.title}
    except Exception as e:
        logger.error(f"Add error: {e}")
        raise HTTPException(status_code=500,detail=str(e))
@router.delete("/{entry_id}")
async def delete_knowledge(entry_id:str,qdrant=Depends(get_qdrant)):
    try:
        await qdrant.delete(entry_id)
        return{"deleted":entry_id}
    except Exception as e:
        logger.error(f"Delete error: {e}")
        raise HTTPException(status_code=500,detail=str(e))