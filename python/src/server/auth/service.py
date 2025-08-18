"""User registration and authentication service."""

from __future__ import annotations

import hashlib
import secrets
from typing import Dict

from .models import User


class AuthError(Exception):
    """Raised when authentication operations fail."""


class AuthService:
    """In-memory authentication backend."""

    def __init__(self) -> None:
        self._users: Dict[str, Dict[str, str]] = {}

    async def register(self, username: str, password: str, role: str = "user") -> User:
        if username in self._users:
            raise AuthError("user exists")
        salt = secrets.token_hex(16)
        hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000).hex()
        self._users[username] = {"salt": salt, "hash": hashed, "role": role}
        return User(username=username, role=role)

    async def authenticate(self, username: str, password: str) -> User:
        user = self._users.get(username)
        if not user:
            raise AuthError("invalid credentials")
        hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), user["salt"].encode(), 100_000).hex()
        if secrets.compare_digest(hashed, user["hash"]):
            return User(username=username, role=user["role"])
        raise AuthError("invalid credentials")


__all__ = ["AuthService", "AuthError"]

