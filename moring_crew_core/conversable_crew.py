from typing import List, Dict, Any
from role import Role
from util.llm_model import llm_model
from config.settings import DEFAULT_MODEL
import asyncio

class ConversableCrew:
    def __init__(self, roles: List[Role], model_index: str = DEFAULT_MODEL):
        self.roles = roles
        self.model_index = model_index
        self.conversation_memory = []  # Add conversation memory

    async def instruction(self, user_input: str) -> str:
        self.conversation_memory.append({"role": "user", "content": user_input})

        
        return response
    
    def run_instruction(self, user_input: str) -> str:
        return asyncio.run(self.instruction(user_input))