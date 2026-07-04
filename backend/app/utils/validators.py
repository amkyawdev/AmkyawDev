import re
from typing import Optional


def validate_skill_name(name: str) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9_-]+$", name))


def sanitize_filename(filename: str) -> str:
    sanitized = filename.replace("/", "_").replace("\\", "_").replace("\0", "")
    sanitized = sanitized.lstrip(".")
    if not sanitized:
        sanitized = "unnamed"
    return sanitized


def validate_language(language: str) -> Optional[str]:
    language_map = {"py": "python", "python": "python", "js": "javascript", "javascript": "javascript", "ts": "typescript", "typescript": "typescript", "go": "go", "golang": "go", "rs": "rust", "rust": "rust", "java": "java", "rb": "ruby", "ruby": "ruby", "cpp": "cpp", "c++": "cpp", "c": "c", "cs": "csharp", "csharp": "csharp", "c#": "csharp", "sh": "bash", "bash": "bash", "sql": "sql", "html": "html", "css": "css", "yaml": "yaml", "json": "json", "md": "markdown", "markdown": "markdown"}
    return language_map.get(language.lower(), language.lower())
