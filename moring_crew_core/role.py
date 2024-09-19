from typing import List, Dict, Any
from util.llm_model import llm_model
from skillset import Skillset
import asyncio

class Role:
    def __init__(self, personal_info: Dict[str, str], skillsets: List[Skillset]):
        self.personal_info = personal_info
        self.skillsets = skillsets

    async def chat(self, user_input: str, conversation_memory: List[Dict[str, str]]) -> str:
        # Use conversation_memory in the response generation
        context = "\n".join([f"{entry['role']}: {entry['content']}" for entry in conversation_memory])
        prompt = f"As {self.personal_info['name']} ({self.personal_info['title']}), {self.personal_info['description']}. Given the conversation history:\n{context}\n\nRespond to the user's input: '{user_input}'"
        
        # Check if any skillset can handle the user input
        for skillset in self.skillsets:
            if skillset.can_handle(user_input):
                response = await skillset._arun(user_input)
                break
        else:
            response = llm_model.get_response("G1", prompt).strip()
        
        return response

    def _get_default_output_parser(self):
        # Implement a default output parser if needed
        return None

    def create_prompt(self, input_variables):
        # Create a prompt using input variables
        return f"As {self.personal_info['name']}, please respond to: {input_variables['input']}"

    @property
    def llm_prefix(self):
        return "Human"

    @property
    def observation_prefix(self):
        return "AI"