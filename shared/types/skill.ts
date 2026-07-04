export interface SkillMetadata {
  name: string;
  description: string;
  path?: string;
  size?: number;
}

export interface SkillContent {
  metadata: SkillMetadata;
  content: string;
}

export interface SkillListResponse {
  skills: SkillMetadata[];
}
