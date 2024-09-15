from typing import List, Dict, Any
from skillset import Skillset

class Role:
    def __init__(self, personal_info: Dict[str, Any], skillsets: List[Skillset]):
        self.personal_info = personal_info
        self.skillsets = skillsets

    def chat(self, user_input: str, conversation_history: List[Dict[str, str]] = None) -> str:
        # Implement chat logic here, using skillsets and conversation history
        context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history]) if conversation_history else ""
        
        response = f"As {self.personal_info['name']}, I received: {user_input}\nContext: {context}\n"
        for skillset in self.skillsets:
            response += f"Using {skillset.name}: {skillset.run(user_input)}\n"
        
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