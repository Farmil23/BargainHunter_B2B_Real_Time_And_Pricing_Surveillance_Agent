from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # API Keys
    OPENAI_API_KEY: str
    BRIGHTDATA_API_KEY: str
    OPENROUTER_API_KEY: str
    PINECONE_API_KEY: str
    
    # DB Configuration
    DATABASE_URI: str
    
    # Project Settings
    PROJECT_NAME: str = "Surveillance Agent API"
    VERSION: str = "1.0.0"
    
    # Pinecone
    PINECONE_INDEX_NAME: str = "surveillance-index"
    PINECONE_DIMENSION: int = 1024
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

settings = Settings()
