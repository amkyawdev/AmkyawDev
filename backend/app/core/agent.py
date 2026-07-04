from typing import Optional
from app.services.openrouter_service import OpenRouterService
from app.core.skill_loader import SkillLoader
from app.core.context_manager import ContextManager
from app.utils.logger import setup_logger
logger=setup_logger(__name__)
class CoderAgent:
    def __init__(self,openrouter_service:OpenRouterService,skill_loader:SkillLoader,context_manager:Optional[ContextManager]=None,skills:Optional[list[str]]=None):
        self.llm=openrouter_service;self.skills=skill_loader;self.context=context_manager or ContextManager();self.requested_skills=skills or[]
    def _load_skills(self,skills:Optional[list[str]])->list[str]:
        sp=[]
        if skills:
            for sn in skills:
                sc=self.skills.load_skill(sn)
                if sc:sp.append(sc)
        return sp
    async def chat(self,messages:list[dict],skills:Optional[list[str]]=None,model:Optional[str]=None)->str:
        sp=self._load_skills(skills)
        sys_prompt=self._build_system_prompt(sp)
        fm=[{"role":"system","content":sys_prompt}]
        fm.extend(self.context.get_context_window(messages))
        response=await self.llm.chat_completion(messages=fm,model=model)
        assistant_message=response["choices"][0]["message"]["content"]
        self.context.add_turn("assistant",assistant_message)
        return assistant_message
    async def generate_code(self,prompt:str,language:str="python",skills:Optional[list[str]]=None,context:Optional[str]=None)->str:
        sp=self._load_skills(skills)
        sys_prompt=self._build_code_generation_prompt(language=language,skill_prompts=sp)
        user_prompt=prompt
        if context:user_prompt=f"Context:\n{context}\n\nTask:\n{prompt}"
        messages=[{"role":"system","content":sys_prompt},{"role":"user","content":user_prompt}]
        response=await self.llm.chat_completion(messages=messages,model=self.llm.default_code_model)
        content=response["choices"][0]["message"]["content"]
        code,explanation=self._extract_code_and_explanation(content,language)
        return code
    async def chat_with_history(self,messages:list[dict],skills:Optional[list[str]]=None)->str:
        return await self.chat(messages,skills)
    async def generate_code_with_context(self,prompt:str,language:str="python",skills:Optional[list[str]]=None,context:Optional[str]=None)->str:
        if context:prompt=f"Context:\n{context}\n\nTask:\n{prompt}"
        return await self.generate_code(prompt,language,skills)
    def _build_system_prompt(self,sp:list[str])->str:
        base="You are an AmkyawDev Tools AI Agent - an expert software developer and coding assistant.\n\nGuidelines:\n- Write clean, readable, well-documented code\n- Use best practices and design patterns\n- Be concise but thorough"
        if sp:base+="\n\n## Loaded Skills\n\n"+"\n\n---\n\n".join(sp)
        return base
    def _build_code_generation_prompt(self,language:str,skill_prompts:list[str])->str:
        prompt=f"You are an expert {language} developer. Generate production-quality code.\n\nRequirements:\n- Write only valid, runnable {language} code\n- Include necessary imports\n- Add type hints and docstrings\n- Handle edge cases\n- Follow {language} best practices\n\nOutput the code in a markdown code block."
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
    async def chat_with_nvidia(self,messages:list[dict],nvidia_service,skills:Optional[list[str]]=None)->str:
        sp=self._load_skills(skills)
        sys_prompt=self._build_system_prompt(sp)
        fm=[{"role":"system","content":sys_prompt}]
        fm.extend(self.context.get_context_window(messages))
        response=await nvidia_service.chat_completion(messages=fm)
        return response["choices"][0]["message"]["content"]