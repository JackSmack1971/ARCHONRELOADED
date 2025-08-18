"""JWT creation and verification utilities."""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt


class JWTError(Exception):
    """Raised when JWT operations fail."""


class JWTService:
    """Handle JWT encoding and decoding."""

    def __init__(self) -> None:
        secret = os.getenv("JWT_SECRET")
        if not secret:
            raise JWTError("JWT_SECRET not set")
        self._secret = secret
        self._alg = os.getenv("JWT_ALG", "HS256")
        self._expire = int(os.getenv("JWT_EXPIRE_MINUTES", "15"))

    def create_token(self, subject: str, role: str) -> str:
        """Create a signed JWT for the given subject."""
        try:
            now = datetime.now(tz=timezone.utc)
            payload: Dict[str, Any] = {
                "sub": subject,
                "role": role,
                "iat": now,
                "exp": now + timedelta(minutes=self._expire),
            }
            return jwt.encode(payload, self._secret, algorithm=self._alg)
        except Exception as exc:  # pragma: no cover - defensive
            raise JWTError("token creation failed") from exc

    def verify_token(self, token: str) -> Dict[str, Any]:
        """Decode and validate a JWT, returning its payload."""
        try:
            return jwt.decode(token, self._secret, algorithms=[self._alg])
        except Exception as exc:
            raise JWTError("token verification failed") from exc


__all__ = ["JWTService", "JWTError"]

