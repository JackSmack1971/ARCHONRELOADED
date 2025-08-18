"""Health check route."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from ..models.base import ResponseModel, ResponseStatus
from ..services.database import DatabaseError, DatabaseService
from . import get_database_service

router = APIRouter(tags=["health"])


@router.get("/health", response_model=ResponseModel[dict[str, str]])
async def health(
    db: DatabaseService = Depends(get_database_service),
) -> ResponseModel[dict[str, str]]:
    """Check database connectivity and report service status."""
    try:
        await db.list_projects()
        return ResponseModel(status=ResponseStatus.SUCCESS, data={"database": "ok"})
    except DatabaseError as exc:
        raise HTTPException(status_code=503, detail="database unavailable") from exc
