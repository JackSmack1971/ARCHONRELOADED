"""User authentication routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from ..auth.jwt import JWTService
from ..auth.models import Token, User, UserCreate
from ..auth.service import AuthError, AuthService
from ..models.base import ResponseModel, ResponseStatus


router = APIRouter(prefix="/auth", tags=["auth"])
_service = AuthService()
_jwt = JWTService()


@router.post("/register", response_model=ResponseModel[User])
async def register(payload: UserCreate) -> ResponseModel[User]:
    """Register a new user."""
    try:
        user = await _service.register(payload.username, payload.password)
        return ResponseModel(status=ResponseStatus.SUCCESS, data=user)
    except AuthError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/login", response_model=ResponseModel[Token])
async def login(payload: UserCreate) -> ResponseModel[Token]:
    """Authenticate a user and return an access token."""
    try:
        user = await _service.authenticate(payload.username, payload.password)
    except AuthError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))
    token = _jwt.create_token(user.username, user.role)
    return ResponseModel(status=ResponseStatus.SUCCESS, data=Token(access_token=token))


__all__ = ["router"]

