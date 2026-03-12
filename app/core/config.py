"""Application configuration."""
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment."""

    api_title: str = "Healthcare Mock API"
    api_version: str = "1.0.0"
    api_description: str = (
        "Standards-aligned mock API for U.S. healthcare administrative workflows. "
        "X12, FHIR R4, and Da Vinci implementation guide alignment documented per route."
    )
    log_level: str = "INFO"

    # Auth0 / JWT (when set, enables real JWT validation; when empty, mock mode accepts any token)
    auth0_domain: str = ""  # AUTH0_DOMAIN
    auth0_issuer: str = ""  # AUTH0_ISSUER
    auth0_audience: str = ""  # AUTH0_AUDIENCE
    auth0_required_scope_execute: str = "execute"  # AUTH0_REQUIRED_SCOPE_EXECUTE
    auth0_required_scope_ai_execute: str = "ai_execute"  # AUTH0_REQUIRED_SCOPE_AI_EXECUTE
    partner_code: str = ""  # PARTNER_CODE

    # Optional: restrict endpoints per deployment (comma-separated). Empty = all allowed.
    allowed_operations: str = ""  # ALLOWED_OPERATIONS

    model_config = {"env_file": ".env", "extra": "ignore"}

    @property
    def jwt_enabled(self) -> bool:
        """True when Auth0 issuer is configured (real JWT validation)."""
        return bool(self.auth0_issuer and self.auth0_issuer.strip())

    @property
    def required_scopes(self) -> list[str]:
        """Scopes required for API access."""
        return [s for s in (self.auth0_required_scope_execute, self.auth0_required_scope_ai_execute) if s]


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()
