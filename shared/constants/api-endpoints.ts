export const API_ENDPOINTS = {
  AGENT_CHAT: "/api/agent/chat",
  AGENT_GENERATE: "/api/agent/generate",
  AGENT_SKILLS: "/api/agent/skills",
  KNOWLEDGE_SEARCH: "/api/knowledge/search",
  KNOWLEDGE_UPSERT: "/api/knowledge/upsert",
  KNOWLEDGE_BATCH_UPSERT: "/api/knowledge/upsert/batch",
  KNOWLEDGE_DELETE: "/api/knowledge/:id",
  FILES_UPLOAD: "/api/files/upload",
  FILES_LIST: "/api/files/list",
  FILES_EXPORT: "/api/files/export",
  TELEGRAM_WEBHOOK: "/api/telegram/webhook",
  HEALTH: "/health",
} as const;

export const DEFAULT_MODELS = {
  OPENROUTER: "anthropic/claude-sonnet-4.5",
  NVIDIA: "meta/llama-3.1-405b-instruct",
} as const;

export const SUPPORTED_LANGUAGES = [
  "python", "javascript", "typescript", "go", "rust", "java", "ruby", "cpp", "c",
  "csharp", "bash", "sql", "html", "css", "yaml", "json", "markdown",
] as const;
