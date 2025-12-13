from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path

# Get the directory where this config file is located (src/)
SRC_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_DIR.parent


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""
    
    # API
    app_name: str = "CampusOps AI"
    debug: bool = False
    
    # OpenAI
    openai_api_key: str
    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "gpt-3.5-turbo"
    
    # ChromaDB - use project root for chroma_db
    chroma_db_path: str = str(PROJECT_ROOT / "chroma_db")
    collection_name: str = "policies"
    
    # RAG Settings
    top_k_chunks: int = 5  # Retrieve more chunks for better context
    llm_temperature: float = 0.3
    
    class Config:
        # Look for .env in both src/ and project root
        env_file = [SRC_DIR / ".env", PROJECT_ROOT / ".env"]
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()
