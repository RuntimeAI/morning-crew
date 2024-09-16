from langchain.tools import BaseTool
from util.llm_model import llm_model
from typing import List, Dict, Any

class Skillset(BaseTool):
    def __init__(self, name: str, description: str):
        super().__init__(name=name, description=description)

    def _run(self, query: str) -> str:
        # Implement the actual functionality of the skillset here
        return f"Processed '{query}' using {self.name}"

    async def _arun(self, query: str) -> str:
        # Implement async version if needed
        return self._run(query)

    def can_handle(self, query: str) -> bool:
        # Use llm_model to determine if this skillset can handle the query
        prompt = f"Can the skillset '{self.name}' handle the following query: '{query}'? Respond with 'yes' or 'no'."
        response = llm_model.get_response("G1", prompt).strip().lower()
        return response == 'yes'