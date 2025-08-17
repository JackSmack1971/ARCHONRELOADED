"""Project management tools for MCP."""

from __future__ import annotations

from typing import Dict
from uuid import uuid4

from pydantic import BaseModel, Field

from .. import ToolExecutionError


class Project(BaseModel):
    """Simple project model."""

    id: str
    name: str
    status: str = "new"


PROJECTS: Dict[str, Project] = {}


class CreateProjectRequest(BaseModel):
    """Request model for creating a project."""

    name: str = Field(..., min_length=1, max_length=100)


async def create_project(params: dict) -> dict:
    """Create a new project."""

    data = CreateProjectRequest(**params)
    project = Project(id=str(uuid4()), name=data.name)
    PROJECTS[project.id] = project
    return project.model_dump()


async def list_projects(_: dict) -> dict:
    """List all projects."""

    return {"projects": [p.model_dump() for p in PROJECTS.values()]}


class StatusRequest(BaseModel):
    """Request model for retrieving project status."""

    project_id: str = Field(..., min_length=1)


async def get_project_status(params: dict) -> dict:
    """Get information about a project."""

    data = StatusRequest(**params)
    project = PROJECTS.get(data.project_id)
    if not project:
        raise ToolExecutionError("Project not found")
    return project.model_dump()


TOOLS = {
    "list_projects": list_projects,
    "create_project": create_project,
    "get_project_status": get_project_status,
}
