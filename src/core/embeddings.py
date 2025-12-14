from openai import OpenAI
from src.config import get_settings


class EmbeddingService:
    """Service for generating text embeddings using OpenAI."""
    
    def __init__(self):
        settings = get_settings()
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.embedding_model
        print(f"✅ Using OpenAI for embeddings (model: {self.model})")
    
    def embed_text(self, text: str) -> list[float]:
        """Generate embedding for a single text."""
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding
    
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts."""
        response = self.client.embeddings.create(
            model=self.model,
            input=texts
        )
        return [item.embedding for item in response.data]
    
