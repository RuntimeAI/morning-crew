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

        # Check if the user input explicitly mentions a role's name or title
        selected_role = None
        role_descriptions = "\n".join([f"{role.personal_info['name']} ({role.personal_info['title']}): {role.personal_info['description']}" for role in self.roles])
        prompt = f"Given the following roles:\n{role_descriptions}\n\nWhich role should handle this instruction: '{user_input}'?, only respond with the role's name"
        selected_role_name = llm_model.get_response(self.model_index, prompt).strip()
        print(f"Selected role name: {selected_role_name}")  
        selected_role = next((role for role in self.roles if role.personal_info['name'].lower() in selected_role_name.lower()), None)

        print(f"selected role: {selected_role.personal_info['name']}")

        if selected_role.personal_info['name']:
            print({selected_role.personal_info['name']})
            print(self.conversation_memory)
            response = await selected_role.chat(user_input, self.conversation_memory)  # Pass conversation_memory to chat method
        else:
            response = await self.general_chat(user_input, role_descriptions)  # Handle general chat

        self.conversation_memory.append({"role": selected_role.personal_info['name'] if selected_role else "general", "content": response})

        return response

    async def general_chat(self, user_input: str, role_descriptions: str) -> str:
        # Handle general or non-task related conversation
        context = "\n".join([f"{entry['role']}: {entry['content']}" for entry in self.conversation_memory])
        prompt = f"Given the conversation history:\n{context}\n\nRoles available:\n{role_descriptions}\n\nRespond to the user's input: '{user_input}'"
        response = llm_model.get_response("G1", prompt).strip()
        return response

    def run_instruction(self, user_input: str) -> str:
        return asyncio.run(self.instruction(user_input))