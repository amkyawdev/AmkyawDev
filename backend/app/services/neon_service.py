import os
from typing import Optional
import asyncpg
from app.utils.logger import setup_logger
logger=setup_logger(__name__)
class PostgresService:
    def __init__(self):self.database_url=os.getenv("PSQL_CMD",os.getenv("DATABASE_URL",os.getenv("NEON_DATABASE_URL","")));self.pool=None
    async def connect(self):
        if not self.database_url:logger.warning("No PostgreSQL URL configured");return
        if self.pool is None:
            try:self.pool=await asyncpg.create_pool(self.database_url,min_size=2,max_size=10);await self._init_tables();logger.info("Connected to PostgreSQL")
            except Exception as e:logger.error(f"PostgreSQL connection failed: {e}");self.pool=None
    async def _init_tables(self):
        async with self.pool.acquire() as conn:
            await conn.execute("CREATE TABLE IF NOT EXISTS conversations (id SERIAL PRIMARY KEY,session_id VARCHAR(255) NOT NULL,role VARCHAR(50) NOT NULL,content TEXT NOT NULL,skill VARCHAR(255),created_at TIMESTAMP DEFAULT NOW());CREATE TABLE IF NOT EXISTS files (id SERIAL PRIMARY KEY,filename VARCHAR(500),path VARCHAR(1000),size BIGINT,content_type VARCHAR(255),skill VARCHAR(255),uploaded_at TIMESTAMP DEFAULT NOW());CREATE TABLE IF NOT EXISTS code_generations (id SERIAL PRIMARY KEY,prompt TEXT,language VARCHAR(50),code TEXT,skill VARCHAR(255),created_at TIMESTAMP DEFAULT NOW());CREATE TABLE IF NOT EXISTS knowledge_entries (id SERIAL PRIMARY KEY,title VARCHAR(500),content TEXT,tags TEXT[],source VARCHAR(255),embedding_id VARCHAR(255),created_at TIMESTAMP DEFAULT NOW(),updated_at TIMESTAMP DEFAULT NOW())")
    async def save_conversation(self,session_id,role,content,skill=None):
        if not self.pool:await self.connect()
        if not self.pool:return
        async with self.pool.acquire() as c:await c.execute("INSERT INTO conversations(session_id,role,content,skill) VALUES($1,$2,$3,$4)",session_id,role,content,skill)
    async def get_conversation(self,session_id,limit=50):
        if not self.pool:await self.connect()
        if not self.pool:return[]
        async with self.pool.acquire() as c:rows=await c.fetch("SELECT role,content,skill,created_at FROM conversations WHERE session_id=$1 ORDER BY created_at DESC LIMIT $2",session_id,limit);return[dict(r)for r in rows]
    async def save_file_record(self,filename,path,size,content_type,skill=None):
        if not self.pool:await self.connect()
        if not self.pool:return
        async with self.pool.acquire() as c:await c.execute("INSERT INTO files(filename,path,size,content_type,skill) VALUES($1,$2,$3,$4,$5)",filename,path,size,content_type,skill)
    async def save_knowledge(self,title,content,tags=None,source=None,embedding_id=None):
        if not self.pool:await self.connect()
        if not self.pool:return
        async with self.pool.acquire() as c:await c.execute("INSERT INTO knowledge_entries(title,content,tags,source,embedding_id) VALUES($1,$2,$3,$4,$5)",title,content,tags or[],source,embedding_id)
    async def search_knowledge(self,query,limit=10):
        if not self.pool:await self.connect()
        if not self.pool:return[]
        async with self.pool.acquire() as c:rows=await c.fetch("SELECT id,title,content,tags,source,created_at FROM knowledge_entries WHERE title ILIKE $1 OR content ILIKE $1 ORDER BY created_at DESC LIMIT $2",f"%{query}%",limit);return[dict(r)for r in rows]
    async def close(self):
        if self.pool:await self.pool.close();logger.info("PostgreSQL connection closed")
NeonService=PostgresService