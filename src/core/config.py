from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/exrai_db"
    
    # API Keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # App Settings
    app_name: str = "Exrai Theme Analyzer"
    debug: bool = False
    environment: str = "development"
    
    # Embeddings
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dimension: int = 384
    
    # Theme Analysis
    similarity_threshold: float = 0.85
    relevance_increment: float = 1.0
    max_themes_per_analysis: int = 10
    
    # API
    api_prefix: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()