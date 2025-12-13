from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""
    
    # API
    app_name: str = "CampusOps AI"
    debug: bool = False
    
    # OpenAI
    openai_api_key: str
    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "gpt-3.5-turbo"
    
    # ChromaDB
    chroma_db_path: str = "./chroma_db"
    collection_name: str = "policies"
    
    # RAG Settings
    top_k_chunks: int = 3
    llm_temperature: float = 0.3
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()
