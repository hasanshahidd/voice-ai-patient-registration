"""
Pydantic settings for environment variable validation.
"""

from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    PORT: int = 3000
    ENVIRONMENT: str = "development"
    
    DATABASE_URL: str
    
    VAPI_API_KEY: str = ""
    VAPI_PHONE_NUMBER_ID: str = ""
    VAPI_WEBHOOK_SECRET: str = ""
    
    OPENAI_API_KEY: str = ""
    
    CORS_ORIGINS: List[str] = ["*"]
    
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
