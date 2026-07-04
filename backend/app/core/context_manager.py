from collections import deque
from app.utils.logger import setup_logger
logger=setup_logger(__name__)
MAX_CONTEXT_MESSAGES=20
MAX_CONTEXT_TOKENS_ESTIMATE=8000
class ContextManager:
    def __init__(self,max_messages:int=MAX_CONTEXT_MESSAGES):
        self.max_messages=max_messages;self.history:deque=deque(maxlen=max_messages);self.metadata:dict={}
    def add_turn(self,role:str,content:str):
        self.history.append({"role":role,"content":content})
    def get_context_window(self,new_messages:list[dict])->list[dict]:
        context=list(self.history)
        for msg in new_messages:
            if msg.get("role")=="user":self.add_turn("user",msg["content"])
        context.extend(new_messages)
        return context
    def set_metadata(self,key:str,value):
        self.metadata[key]=value
    def get_metadata(self,key:str,default=None):
        return self.metadata.get(key,default)
    def clear(self):
        self.history.clear();self.metadata.clear();logger.info("Context cleared")
    def summarize(self)->str:
        if not self.history:return"No conversation history."
        user_messages=[m for m in self.history if m["role"]=="user"]
        return f"Conversation with {len(user_messages)} user messages, {len(self.history)} total turns."