import os
from typing import Optional
from openai import AsyncOpenAI
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class OpenRouterService:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY", "")
        self.base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        self.default_model = os.getenv("OPENROUTER_DEFAULT_MODEL", "anthropic/claude-sonnet-4.5")
        self.client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url) if self.api_key else None

    async def chat_completion(self, messages: list[dict], model: Optional[str] = None, temperature: float = 0.7, max_tokens: int = 4096) -> dict:
        if not self.client:
            raise ValueError("OpenRouter API key not configured")
        model_name = model or self.default_model
        logger.info(f"Calling OpenRouter with model: {model_name}")
        response = await self.client.chat.completions.create(model=model_name, messages=messages, temperature=temperature, max_tokens=max_tokens)
        return response.model_dump()

    async def stream_chat_completion(self, messages: list[dict], model: Optional[str] = None, temperature: float = 0.7, max_tokens: int = 4096):
        if not self.client:
            raise ValueError("OpenRouter API key not configured")
        model_name = model or self.default_model
        stream = await self.client.chat.completions.create(model=model_name, messages=messages, temperature=temperature, max_tokens=max_tokens, stream=True)
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
