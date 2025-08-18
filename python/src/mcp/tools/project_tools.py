"""Project management tools for MCP."""

from __future__ import annotations

from typing import Any, Dict
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .. import ToolExecutionError
from .. import deps
from src.server.models.project import Project, ProjectStatus
from src.server.services.database import DatabaseError


class CreateProjectRequest(BaseModel):
    """Input schema for creating projects."""

    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class StatusRequest(BaseModel):
    """Input schema for project status lookup."""

    project_id: UUID = Field(...)


async def create_project(params: Dict[str, Any]) -> Dict[str, Any]:
    """Create a project using the shared database service."""

    data = CreateProjectRequest(**params)
    project = Project(
        id=uuid4(),
        name=data.name,
        description=data.description or "",
        status=ProjectStatus.ACTIVE,
        settings={},
    )
    try:
        created = await deps.db_service.create_project(project)
    except DatabaseError as exc:
        raise ToolExecutionError("create_project failed") from exc
    return created.model_dump(mode="json")


async def list_projects(_: Dict[str, Any]) -> Dict[str, Any]:
    """Return all projects from the database."""

    projects = await deps.db_service.list_projects()
    return {"projects": [p.model_dump(mode="json") for p in projects]}


async def get_project_status(params: Dict[str, Any]) -> Dict[str, Any]:
    """Fetch a project's status by ID."""

    data = StatusRequest(**params)
    project = await deps.db_service.get_project(data.project_id)
    if not project:
        raise ToolExecutionError("project not found")
    return project.model_dump(mode="json")


TOOLS = {
    "create_project": create_project,
    "list_projects": list_projects,
    "get_project_status": get_project_status,
}
