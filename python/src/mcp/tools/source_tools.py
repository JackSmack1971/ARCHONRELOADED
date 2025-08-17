"""Knowledge source management tools."""

from __future__ import annotations

from typing import Dict, List

from pydantic import BaseModel, Field

from .. import ToolExecutionError
from .project_tools import PROJECTS

PROJECT_SOURCES: Dict[str, List[str]] = {}


class AddSourceRequest(BaseModel):
    """Request model for adding a source to a project."""

    project_id: str = Field(..., min_length=1)
    source: str = Field(..., min_length=1, max_length=200)


async def add_source(params: dict) -> dict:
    """Add a knowledge source to a project."""

    data = AddSourceRequest(**params)
    if data.project_id not in PROJECTS:
        raise ToolExecutionError("Project not found")
    PROJECT_SOURCES.setdefault(data.project_id, []).append(data.source)
    return {"sources": PROJECT_SOURCES[data.project_id]}


TOOLS = {"add_source": add_source}
