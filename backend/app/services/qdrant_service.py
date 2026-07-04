import os
import hashlib
from typing import Optional
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
EMBEDDING_DIM = 1536


class QdrantService:
    def __init__(self):
        self.url = os.getenv("QDRANT_URL", "http://localhost:6333")
        self.api_key = os.getenv("QDRANT_API_KEY", "")
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "ai-brain-coder")
        self.client = AsyncQdrantClient(url=self.url, api_key=self.api_key)

    async def ensure_collection(self):
        collections = await self.client.get_collections()
        collection_names = [c.name for c in collections.collections]
        if self.collection_name not in collection_names:
            await self.client.create_collection(collection_name=self.collection_name, vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE))
            logger.info(f"Created collection: {self.collection_name}")

    async def search(self, query: str, skill_filter: Optional[str] = None, limit: int = 10) -> list[dict]:
        await self.ensure_collection()
        query_vector = await self._embed(query)
        query_filter = None
        if skill_filter:
            query_filter = Filter(must=[FieldCondition(key="skill", match=MatchValue(value=skill_filter))])
        results = await self.client.search(collection_name=self.collection_name, query_vector=query_vector, limit=limit, query_filter=query_filter)
        return [{"id": hit.id, "score": hit.score, "content": hit.payload.get("content", ""), "metadata": hit.payload.get("metadata", {}), "skill": hit.payload.get("skill", "")} for hit in results]

    async def upsert(self, entry_id: str, content: str, metadata: Optional[dict] = None, skill: Optional[str] = None):
        await self.ensure_collection()
        vector = await self._embed(content)
        point = PointStruct(id=entry_id, vector=vector, payload={"content": content, "metadata": metadata or {}, "skill": skill or ""})
        await self.client.upsert(collection_name=self.collection_name, points=[point])
        logger.info(f"Upserted knowledge entry: {entry_id}")

    async def delete(self, entry_id: str):
        await self.client.delete(collection_name=self.collection_name, points_selector=[entry_id])
        logger.info(f"Deleted knowledge entry: {entry_id}")

    async def _embed(self, text: str) -> list[float]:
        hash_bytes = hashlib.sha256(text.encode()).digest()
        vector = []
        for i in range(EMBEDDING_DIM):
            byte_val = hash_bytes[i % len(hash_bytes)]
            vector.append((byte_val / 255.0) * 2 - 1)
        return vector
