from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    
    # API Keys
    GEMINI_API_KEY: str
    
    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str
    
    # Environment
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

@lru_cache()
def get_settings():
    return Settings()
