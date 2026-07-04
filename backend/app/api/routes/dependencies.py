from fastapi import Depends
from app.services.openrouter_service import OpenRouterService
from app.services.qdrant_service import QdrantService
from app.services.neon_service import NeonService
from app.services.elevenlabs_service import ElevenLabsService
from app.services.nvidia_service import NvidiaService
from app.core.skill_loader import SkillLoader


_openrouter: OpenRouterService | None = None
_qdrant: QdrantService | None = None
_neon: NeonService | None = None
_elevenlabs: ElevenLabsService | None = None
_nvidia: NvidiaService | None = None
_skill_loader: SkillLoader | None = None


def get_openrouter() -> OpenRouterService:
    global _openrouter
    if _openrouter is None:
        _openrouter = OpenRouterService()
    return _openrouter


def get_qdrant() -> QdrantService:
    global _qdrant
    if _qdrant is None:
        _qdrant = QdrantService()
    return _qdrant


def get_neon() -> NeonService:
    global _neon
    if _neon is None:
        _neon = NeonService()
    return _neon


def get_elevenlabs() -> ElevenLabsService:
    global _elevenlabs
    if _elevenlabs is None:
        _elevenlabs = ElevenLabsService()
    return _elevenlabs


def get_nvidia() -> NvidiaService:
    global _nvidia
    if _nvidia is None:
        _nvidia = NvidiaService()
    return _nvidia


def get_skill_loader() -> SkillLoader:
    global _skill_loader
    if _skill_loader is None:
        _skill_loader = SkillLoader()
    return _skill_loader
