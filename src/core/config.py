"""
Core configuration using Pydantic Settings.
Centralizes all environment variables and application settings.
"""
import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Database
    DATABASE_URL: str
    
    # Kafka
    KAFKA_BROKER_URL: str = "localhost:9092"
    
    # Application
    PROJECT_NAME: str = "EventPulse"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    BACKEND_CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000"

    # Uvicorn
    UVICORN_HOST: str = "[IP_ADDRESS]"
    UVICORN_PORT: int = 8000
    UVICORN_RELOAD: bool = True


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings instance to avoid re-reading .env file.
    """
    return Settings()


# Global settings instance
settings = get_settings()
