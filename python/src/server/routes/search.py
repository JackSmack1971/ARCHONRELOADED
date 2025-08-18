"""Search endpoint for similarity queries."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from ..models.base import ResponseModel, ResponseStatus
from ..models.document import Document
from ..models.query import Query
from ..services.database import DatabaseError, DatabaseService
from ..services.embedding import EmbeddingGenerationError, generate_embedding
from ..socket import broadcast_search_completed, BroadcastError
from . import get_database_service
from loguru import logger

router = APIRouter(tags=["search"])


@router.post("/search", response_model=ResponseModel[List[Document]], status_code=status.HTTP_200_OK)
async def search(
    query: Query, db: DatabaseService = Depends(get_database_service)
) -> ResponseModel[List[Document]]:
    try:
        embedding = await generate_embedding(query.query_text)
        results = await db.vector_search(embedding, query)
        project_id = str(query.filters.get("project_id", ""))
        if project_id:
            try:
                await broadcast_search_completed(
                    project_id,
                    {"query": query.query_text, "results": results},
                )
            except BroadcastError:
                logger.warning("search broadcast failed", project_id=project_id)
        return ResponseModel(status=ResponseStatus.SUCCESS, data=results)
    except (EmbeddingGenerationError, DatabaseError) as exc:
        raise HTTPException(status_code=500, detail="search failed") from exc
