"""Document search and retrieval tools."""

from __future__ import annotations

from typing import Any, Dict
from uuid import UUID

from pydantic import BaseModel, Field

from .. import ToolExecutionError, deps
from src.server.models.query import Query
from src.server.services.database import DatabaseError
from src.server.services.embedding import generate_embedding


class SearchRequest(BaseModel):
    """Input for document search."""

    query: str = Field(..., min_length=1)
    match_count: int = Field(5, ge=1, le=20)


class DocumentRequest(BaseModel):
    """Input for retrieving a document by ID."""

    document_id: UUID = Field(...)


async def search_documents(params: Dict[str, Any]) -> Dict[str, Any]:
    """Search documents via vector similarity."""

    data = SearchRequest(**params)
    embedding = await generate_embedding(data.query)
    query = Query(query_text=data.query, match_count=data.match_count)
    try:
        docs = await deps.db_service.vector_search(embedding, query)
    except DatabaseError as exc:
        raise ToolExecutionError("search failed") from exc
    return {"documents": [d.model_dump(mode="json") for d in docs]}


async def get_document(params: Dict[str, Any]) -> Dict[str, Any]:
    """Retrieve a document by its identifier."""

    data = DocumentRequest(**params)
    doc = await deps.db_service.get_document(data.document_id)
    if not doc:
        raise ToolExecutionError("document not found")
    return doc.model_dump(mode="json")


TOOLS = {
    "search_documents": search_documents,
    "get_document": get_document,
}
