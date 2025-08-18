"""Authentication data models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class User(BaseModel):
    """Authenticated user representation."""

    username: str
    role: str = "user"


class UserCreate(BaseModel):
    """Payload for user registration and login."""

    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=128)


class Token(BaseModel):
    """Access token response."""

    access_token: str
    token_type: str = "bearer"


__all__ = ["User", "UserCreate", "Token"]

