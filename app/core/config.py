"""Application configuration."""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings from environment."""

    api_title: str = "Healthcare Mock API"
    api_version: str = "1.0.0"
    api_description: str = (
        "Standards-aligned mock API for U.S. healthcare administrative workflows. "
        "X12, FHIR R4, and Da Vinci implementation guide alignment documented per route."
    )
    log_level: str = "INFO"

    model_config = {"env_file": ".env", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()
