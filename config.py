from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str = "sqlite:///./books.db"
    redis_url: str = "redis://localhost:6379"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cache_ttl: int = 300  # 5 minutes
    
    class Config:
        env_file = ".env"

settings = Settings()