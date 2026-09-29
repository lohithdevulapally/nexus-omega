"""Application Configuration Module

Uses pydantic-settings to manage and validate environment variables.
"""

from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application Info
    APP_NAME: str = "NEXUS-Ω"
    APP_VERSION: str = "0.1.0"
    APP_ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # PostgreSQL Database
    DATABASE_URL: str = "postgresql://nexus:nexus_password@localhost:5432/nexus"

    # Redis Cache / Message Broker
    REDIS_URL: str = "redis://localhost:6379/0"

    # Hindsight Organizational Memory Engine
    HINDSIGHT_URL: str = "http://localhost:8888"
    HINDSIGHT_BANK_ID: str = "nexus-demo"
    HINDSIGHT_BANK_NAME: str = "NEXUS Organizational Memory"
    HINDSIGHT_API_KEY: Optional[str] = None

    # LLM Settings
    LLM_PROVIDER: str = "mock"  # "openai", "gemini", "anthropic", "mock"
    LLM_API_KEY: Optional[str] = None
    LLM_MODEL: str = "gpt-4o-mini"

    model_config = SettingsConfigDict(
        env_file=(".env", "backend/.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
