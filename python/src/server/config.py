"""Configuration module for the server.

Uses `pydantic-settings` to load and validate environment variables. Values
are loaded from a `.env` file if present and can be overridden via the
environment. All settings are validated at import time to avoid runtime
misconfiguration.
"""

from __future__ import annotations

from typing import List
from dotenv import load_dotenv
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings sourced from the environment."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    server_port: int = Field(default=8080, ge=1, le=65535)
    cors_origins: List[str] = Field(default_factory=lambda: ["http://localhost:3000"])

    @field_validator("cors_origins", mode="before")
    @classmethod
    def split_origins(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str):
            return [o.strip() for o in v.split(",") if o.strip()]
        return v


settings = Settings()


__all__ = ["settings", "Settings"]
