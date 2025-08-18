"""Project CRUD routes."""
from __future__ import annotations

from typing import List, Optional, Dict, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field

from ..models.base import ResponseModel, ResponseStatus
from ..models.project import Project, ProjectStatus
from ..services.database import DatabaseError, DatabaseService
from . import get_database_service


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[ProjectStatus] = None
    settings: Optional[Dict[str, Any]] = None


router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ResponseModel[Project], status_code=status.HTTP_201_CREATED)
async def create_project(
    project: Project, db: DatabaseService = Depends(get_database_service)
) -> ResponseModel[Project]:
    """Create a new project."""
    try:
        created = await db.create_project(project)
        return ResponseModel(status=ResponseStatus.SUCCESS, data=created)
    except DatabaseError as exc:
        raise HTTPException(status_code=500, detail="create failed") from exc


@router.get("/", response_model=ResponseModel[List[Project]])
async def list_projects(
    db: DatabaseService = Depends(get_database_service),
) -> ResponseModel[List[Project]]:
    """List all projects."""
    projects = await db.list_projects()
    return ResponseModel(status=ResponseStatus.SUCCESS, data=projects)


@router.get("/{project_id}", response_model=ResponseModel[Project])
async def get_project(
    project_id: UUID = Path(...),
    db: DatabaseService = Depends(get_database_service),
) -> ResponseModel[Project]:
    """Retrieve a project by ID."""
    project = await db.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="project not found")
    return ResponseModel(status=ResponseStatus.SUCCESS, data=project)


@router.put("/{project_id}", response_model=ResponseModel[Project])
async def update_project(
    project_id: UUID = Path(...),
    data: ProjectUpdate | None = None,
    db: DatabaseService = Depends(get_database_service),
) -> ResponseModel[Project]:
    """Update project fields."""
    payload = data.model_dump(exclude_none=True) if data else {}
    updated = await db.update_project(project_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="project not found")
    return ResponseModel(status=ResponseStatus.SUCCESS, data=updated)


@router.delete("/{project_id}", response_model=ResponseModel[dict[str, bool]])
async def delete_project(
    project_id: UUID = Path(...),
    db: DatabaseService = Depends(get_database_service),
) -> ResponseModel[dict[str, bool]]:
    """Delete a project."""
    ok = await db.delete_project(project_id)
    if not ok:
        raise HTTPException(status_code=404, detail="project not found")
    return ResponseModel(status=ResponseStatus.SUCCESS, data={"deleted": True})
