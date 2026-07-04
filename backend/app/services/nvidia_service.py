import os
from typing import Optional
from openai import AsyncOpenAI
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class NvidiaService:
    def __init__(self):
        self.api_key = os.getenv("NVIDIA_API_KEY", "")
        self.base_url = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
        self.client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url) if self.api_key else None

    async def chat_completion(self, messages: list[dict], model: str = "meta/llama-3.1-405b-instruct", temperature: float = 0.7, max_tokens: int = 4096) -> dict:
        if not self.client:
            raise ValueError("NVIDIA API key not configured")
        logger.info(f"Calling NVIDIA NIM with model: {model}")
        response = await self.client.chat.completions.create(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens)
        return response.model_dump()
