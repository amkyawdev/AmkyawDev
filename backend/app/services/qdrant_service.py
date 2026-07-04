import os
from typing import Optional
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance,VectorParams,PointStruct,Filter,FieldCondition,MatchValue
from app.utils.logger import setup_logger
logger=setup_logger(__name__)
EMBEDDING_DIM=1536
class QdrantService:
    def __init__(self):
        self.url=os.getenv("QDRANT_URL","http://localhost:6333")
        self.api_key=os.getenv("QDRANT_API_KEY","")
        self.collection_name=os.getenv("QDRANT_COLLECTION_NAME","amkyawdev-tools")
        self.client=AsyncQdrantClient(url=self.url,api_key=self.api_key)
    async def ensure_collection(self):
        collections=await self.client.get_collections()
        names=[c.name for c in collections.collections]
        if self.collection_name not in names:
            await self.client.create_collection(collection_name=self.collection_name,vectors_config=VectorParams(size=EMBEDDING_DIM,distance=Distance.COSINE))
            logger.info(f"Created collection: {self.collection_name}")
    async def search(self,query:str,skill_filter:Optional[str]=None,limit:int=10)->list[dict]:
        await self.ensure_collection()
        qv=await self._embed(query)
        qf=None
        if skill_filter:qf=Filter(must=[FieldCondition(key="skill",match=MatchValue(value=skill_filter))])
        results=await self.client.search(collection_name=self.collection_name,query_vector=qv,limit=limit,query_filter=qf)
        return[{"id":h.id,"score":h.score,"content":h.payload.get("content",""),"metadata":h.payload.get("metadata",{}),"skill":h.payload.get("skill","")}for h in results]
    async def upsert(self,entry_id:str,content:str,metadata:Optional[dict]=None,skill:Optional[str]=None):
        await self.ensure_collection()
        vector=await self._embed(content)
        point=PointStruct(id=entry_id,vector=vector,payload={"content":content,"metadata":metadata or{},"skill":skill or""})
        await self.client.upsert(collection_name=self.collection_name,points=[point])
        logger.info(f"Upserted knowledge entry: {entry_id}")
    async def delete(self,entry_id:str):
        await self.client.delete(collection_name=self.collection_name,points_selector=[entry_id])
        logger.info(f"Deleted knowledge entry: {entry_id}")
    async def _embed(self,text:str)->list[float]:
        import hashlib
        hb=hashlib.sha256(text.encode()).digest()
        return[(hb[i%len(hb)]/255.0)*2-1 for i in range(EMBEDDING_DIM)]