"""Authentication dependencies for FastAPI routes."""

from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .jwt import JWTError, JWTService
from .models import User


bearer = HTTPBearer()
jwt_service = JWTService()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
) -> User:
    """Return the current user from the Authorization header."""
    try:
        payload = jwt_service.verify_token(credentials.credentials)
        return User(username=payload["sub"], role=payload.get("role", "user"))
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)
        )


def require_role(role: str):
    """Create a dependency enforcing a specific user role."""

    async def checker(user: User = Depends(get_current_user)) -> User:
        if user.role != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="insufficient permissions"
            )
        return user

    return checker


__all__ = ["get_current_user", "require_role"]

