"""Retrieval-Augmented Generation tools."""

from __future__ import annotations

from pydantic import BaseModel, Field

from .. import ToolExecutionError
from .source_tools import PROJECT_SOURCES


class QueryRequest(BaseModel):
    """Request model for knowledge queries."""

    project_id: str = Field(..., min_length=1)
    query: str = Field(..., min_length=1, max_length=200)


async def query_knowledge(params: dict) -> dict:
    """Query the knowledge base for a project."""

    data = QueryRequest(**params)
    sources = PROJECT_SOURCES.get(data.project_id)
    if not sources:
        raise ToolExecutionError("No sources for project")
    matches = [s for s in sources if data.query.lower() in s.lower()]
    return {"matches": matches}


TOOLS = {"query_knowledge": query_knowledge}
