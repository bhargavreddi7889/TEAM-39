from openai import OpenAI
from campusops.config import get_settings


class LLMService:
    """Service for generating responses using OpenAI LLM."""
    
    def __init__(self):
        settings = get_settings()
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.llm_model
        self.temperature = settings.llm_temperature
    
    def generate(self, prompt: str) -> str:
        """Generate a response from the LLM."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature
        )
        return response.choices[0].message.content
