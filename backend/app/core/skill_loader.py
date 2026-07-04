import os,re
from pathlib import Path
from typing import Optional
from app.utils.logger import setup_logger
logger=setup_logger(__name__)
SKILLS_DIR=Path(os.getenv("SKILLS_DIR",str(Path(__file__).parent.parent.parent/".amkyaw")))
class SkillLoader:
    def __init__(self,skills_dir:Optional[Path]=None):
        self.skills_dir=skills_dir or SKILLS_DIR;self._cache:dict[str,str]={}
        logger.info(f"SkillLoader initialized with dir: {self.skills_dir}")
    def list_skills(self)->list[dict]:
        skills=[]
        if not self.skills_dir.exists():return skills
        for fp in self.skills_dir.glob("*.md"):
            s=self._parse_skill_file(fp)
            if s:skills.append(s)
        return skills
    def load_skill(self,skill_name:str)->Optional[str]:
        if skill_name in self._cache:return self._cache[skill_name]
        fp=self.skills_dir/f"{skill_name}.md"
        if not fp.exists():logger.warning(f"Skill not found: {skill_name}");return None
        try:
            content=fp.read_text(encoding="utf-8");self._cache[skill_name]=content;return content
        except Exception as e:logger.error(f"Error loading skill {skill_name}: {e}");return None
    def reload(self):
        self._cache.clear();logger.info("Skill cache cleared")
    def _parse_skill_file(self,fp:Path)->Optional[dict]:
        try:
            content=fp.read_text(encoding="utf-8");name=fp.stem;desc=""
            for line in content.split("\n"):
                if line.startswith("# description:"):desc=line.replace("# description:","").strip()
                elif line.startswith("#"):continue
                else:break
            return{"name":name,"description":desc or f"Skill: {name}","path":str(fp),"size":len(content)}
        except Exception as e:logger.error(f"Error parsing skill file {fp}: {e}");return None