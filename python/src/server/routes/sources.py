"""Source CRUD routes."""
from __future__ import annotations

from typing import List, Optional, Dict, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel

from ..models.base import ResponseModel, ResponseStatus
from ..models.source import Source, SourceStatus, SourceType
from ..services.database import DatabaseError, DatabaseService
from . import get_database_service


class SourceUpdate(BaseModel):
    type: Optional[SourceType] = None
    url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    status: Optional[SourceStatus] = None


router = APIRouter(prefix="/sources", tags=["sources"])


@router.post("/", response_model=ResponseModel[Source], status_code=status.HTTP_201_CREATED)
async def create_source(
    source: Source, db: DatabaseService = Depends(get_database_service)
) -> ResponseModel[Source]:
    """Create a new source."""
    try:
        created = await db.create_source(source)
        return ResponseModel(status=ResponseStatus.SUCCESS, data=created)
    except DatabaseError as exc:
        raise HTTPException(status_code=500, detail="create failed") from exc


@router.get("/project/{project_id}", response_model=ResponseModel[List[Source]])
async def list_sources(
    project_id: UUID = Path(...),
    db: DatabaseService = Depends(get_database_service),
) -> ResponseModel[List[Source]]:
    """List sources for a project."""
    sources = await db.list_sources(project_id)
    return ResponseModel(status=ResponseStatus.SUCCESS, data=sources)


@router.get("/{source_id}", response_model=ResponseModel[Source])
async def get_source(
    source_id: UUID = Path(...),
    db: DatabaseService = Depends(get_database_service),
) -> ResponseModel[Source]:
    """Retrieve a source by ID."""
    source = await db.get_source(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="source not found")
    return ResponseModel(status=ResponseStatus.SUCCESS, data=source)


@router.put("/{source_id}", response_model=ResponseModel[Source])
async def update_source(
    source_id: UUID = Path(...),
    data: SourceUpdate | None = None,
    db: DatabaseService = Depends(get_database_service),
) -> ResponseModel[Source]:
    """Update source fields."""
    payload = data.model_dump(exclude_none=True) if data else {}
    updated = await db.update_source(source_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="source not found")
    return ResponseModel(status=ResponseStatus.SUCCESS, data=updated)


@router.delete("/{source_id}", response_model=ResponseModel[dict[str, bool]])
async def delete_source(
    source_id: UUID = Path(...),
    db: DatabaseService = Depends(get_database_service),
) -> ResponseModel[dict[str, bool]]:
    """Delete a source."""
    ok = await db.delete_source(source_id)
    if not ok:
        raise HTTPException(status_code=404, detail="source not found")
    return ResponseModel(status=ResponseStatus.SUCCESS, data={"deleted": True})
