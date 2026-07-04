export interface ChatMessage {
  role: "system" | "user" | "assistant";
  content: string;
}

export interface ChatRequest {
  messages: ChatMessage[];
  skills?: string[];
  model?: string;
  stream?: boolean;
}

export interface ChatResponse {
  message: string;
  skills_used: string[];
  tokens_used: number;
}

export interface CodeGenerationRequest {
  prompt: string;
  language: string;
  skills?: string[];
  context?: string;
  model?: string;
}

export interface CodeGenerationResponse {
  code: string;
  language: string;
  explanation?: string;
  file_path?: string;
}
