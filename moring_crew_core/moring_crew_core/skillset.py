from langchain.tools import BaseTool
from util.llm_model import llm_model


class Skillset(BaseTool):
    def __init__(self, name: str, description: str):
        super().__init__(name=name, description=description)

    def _run(self, query: str) -> str:
        # Implement the actual functionality of the skillset here
        return f"Processed '{query}' using {self.name}"

    async def _arun(self, query: str) -> str:
        # Implement async version if needed
        return self._run(query)