import os
from typing import Optional
from elevenlabs import AsyncElevenLabs
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class ElevenLabsService:
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY", "")
        self.voice_id = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
        self.client = AsyncElevenLabs(api_key=self.api_key) if self.api_key else None

    async def text_to_speech(self, text: str, voice_id: Optional[str] = None, model_id: str = "eleven_monolingual_v1") -> bytes:
        if not self.client:
            raise ValueError("ElevenLabs API key not configured")
        voice = voice_id or self.voice_id
        logger.info(f"Generating TTS with voice: {voice}")
        audio = await self.client.generate(text=text, voice=voice, model=model_id)
        audio_bytes = b""
        async for chunk in audio:
            audio_bytes += chunk
        return audio_bytes

    async def list_voices(self) -> list[dict]:
        if not self.client:
            raise ValueError("ElevenLabs API key not configured")
        voices = await self.client.voices.get_all()
        return [{"id": v.voice_id, "name": v.name} for v in voices.voices]
