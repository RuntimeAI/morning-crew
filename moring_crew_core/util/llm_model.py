from openai import OpenAI
from config.settings import MODEL_MAPPING, OPENAI_API_KEY

class LLMModel:
    def __init__(self):
        self.model_mapping = MODEL_MAPPING
        self.models = {}
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def get_model(self, model_index):
        if model_index not in self.model_mapping:
            raise ValueError(f"Invalid model index: {model_index}")

        if model_index not in self.models:
            self.models[model_index] = self.model_mapping[model_index]

        return self.models[model_index]

    def get_response(self, model_index, prompt):
        model = self.get_model(model_index)
        
        if model_index == 'E1':
            # Handle embeddings separately
            response = self.client.embeddings.create(
                model=model,
                input=prompt
            )
            return response.data[0].embedding
        else:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content

# Singleton instance
llm_model = LLMModel()