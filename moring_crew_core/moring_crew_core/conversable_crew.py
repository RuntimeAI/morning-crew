from typing import List, Dict, Any
from role import Role
from util.llm_model import llm_model
from config.settings import DEFAULT_MODEL

class ConversableCrew:
    def __init__(self, roles: List[Role], model_index: str = DEFAULT_MODEL):
        self.roles = roles
        self.model_index = model_index
        self.conversation_memory = []  # Add conversation memory

    def instruction(self, user_input: str) -> str:
        self.conversation_memory.append({"role": "user", "content": user_input})

        role_descriptions = "\n".join([f"{role.personal_info['name']}: {role.personal_info['description']}" for role in self.roles])
        prompt = f"Given the following roles:\n{role_descriptions}\n\nWhich role should handle this instruction: '{user_input}'?"
        
        selected_role_name = llm_model.get_response(self.model_index, prompt).strip()
        selected_role = next((role for role in self.roles if role.personal_info['name'] == selected_role_name), self.roles[0])

        self.conversation_memory.append({"role": "user", "content": user_input})
        response = selected_role.chat(user_input, self.conversation_history)
        self.conversation_memory.append({"role": selected_role.personal_info['name'], "content": response})

        return response