from typing import Optional
from app.services.openrouter_service import OpenRouterService
from app.core.skill_loader import SkillLoader
from app.core.context_manager import ContextManager
from app.utils.logger import setup_logger
logger=setup_logger(__name__)
class CoderAgent:
    def __init__(self,openrouter_service:OpenRouterService,skill_loader:SkillLoader,context_manager:Optional[ContextManager]=None,skills:Optional[list[str]]=None):
        self.llm=openrouter_service;self.skills_loader=skill_loader;self.context=context_manager or ContextManager();self.requested_skills=skills or[]
    async def chat(self,messages:list[dict],skills:Optional[list[str]]=None,model:Optional[str]=None)->str:
        skill_prompts=[]
        if skills:
            for sn in skills:
                sc=self.skills_loader.load_skill(sn)
                if sc:skill_prompts.append(sc)
        system_prompt=self._build_system_prompt(skill_prompts)
        full_messages=[{"role":"system","content":system_prompt}]
        full_messages.extend(self.context.get_context_window(messages))
        response=await self.llm.chat_completion(messages=full_messages,model=model)
        assistant_message=response["choices"][0]["message"]["content"]
        self.context.add_turn("assistant",assistant_message)
        return assistant_message
    async def generate_code(self,prompt:str,language:str="python",skills:Optional[list[str]]=None)->str:
        skill_prompts=[]
        if skills:
            for sn in skills:
                sc=self.skills_loader.load_skill(sn)
                if sc:skill_prompts.append(sc)
        system_prompt=self._build_code_generation_prompt(language=language,skill_prompts=skill_prompts)
        messages=[{"role":"system","content":system_prompt},{"role":"user","content":prompt}]
        response=await self.llm.chat_completion(messages=messages)
        content=response["choices"][0]["message"]["content"]
        code,explanation=self._extract_code_and_explanation(content,language)
        return code
    def _build_system_prompt(self,skill_prompts:list[str])->str:
        base="You are an AmkyawDev Tools AI Agent - an expert software developer. Write clean, readable, well-documented code. Use best practices. Be concise but thorough."
        if skill_prompts:base+="\n\n## Loaded Skills\n\n"+"\n\n---\n\n".join(skill_prompts)
        return base
    def _build_code_generation_prompt(self,language:str,skill_prompts:list[str])->str:
        prompt=f"You are an expert {language} developer. Generate production-quality code. Output in a markdown code block."
        if skill_prompts:prompt+="\n\n## Special Instructions\n\n"+"\n\n---\n\n".join(skill_prompts)
        return prompt
    def _extract_code_and_explanation(self,content:str,language:str)->tuple[str,str]:
        import re
        pattern=rf"```(?:{language})?\s*\n(.*?)```"
        matches=re.findall(pattern,content,re.DOTALL)
        if matches:return matches[0].strip(),re.sub(pattern,"",content,flags=re.DOTALL).strip()
        generic=re.findall(r"```\s*\n(.*?)```",content,re.DOTALL)
        if generic:return generic[0].strip(),re.sub(r"```\s*\n(.*?)```","",content,flags=re.DOTALL).strip()
        return content,""
    async def chat_with_history(self,messages:list[dict],skills:Optional[list[str]]=None)->str:
        return await self.chat(messages,skills)
    async def generate_code_with_context(self,prompt:str,language:str="python",skills:Optional[list[str]]=None,context:Optional[str]=None)->str:
        if context:prompt=f"Context:\n{context}\n\nTask:\n{prompt}"
        return await self.generate_code(prompt,language,skills)