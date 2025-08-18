"""Document CRUD and search routes."""
from __future__ import annotations

from typing import List, Optional, Dict, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel

from ..models.base import ResponseModel, ResponseStatus
from ..models.document import Document
from ..models.query import Query
from ..services.database import DatabaseError, DatabaseService
from . import get_database_service


class DocumentUpdate(BaseModel):
    content: Optional[str] = None
    embeddings: Optional[List[float]] = None
    metadata: Optional[Dict[str, Any]] = None


class SearchRequest(BaseModel):
    embedding: List[float]
    query: Query


router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/", response_model=ResponseModel[Document], status_code=status.HTTP_201_CREATED)
async def create_document(
    doc: Document, db: DatabaseService = Depends(get_database_service)
) -> ResponseModel[Document]:
    """Create a document."""
    try:
        created = await db.create_document(doc)
        return ResponseModel(status=ResponseStatus.SUCCESS, data=created)
    except DatabaseError as exc:
        raise HTTPException(status_code=500, detail="create failed") from exc


@router.get("/{doc_id}", response_model=ResponseModel[Document])
async def get_document(
    doc_id: UUID = Path(...),
    db: DatabaseService = Depends(get_database_service),
) -> ResponseModel[Document]:
    """Retrieve a document."""
    doc = await db.get_document(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="document not found")
    return ResponseModel(status=ResponseStatus.SUCCESS, data=doc)


@router.put("/{doc_id}", response_model=ResponseModel[Document])
async def update_document(
    doc_id: UUID = Path(...),
    data: DocumentUpdate | None = None,
    db: DatabaseService = Depends(get_database_service),
) -> ResponseModel[Document]:
    """Update a document."""
    payload = data.model_dump(exclude_none=True) if data else {}
    updated = await db.update_document(doc_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="document not found")
    return ResponseModel(status=ResponseStatus.SUCCESS, data=updated)


@router.delete("/{doc_id}", response_model=ResponseModel[dict[str, bool]])
async def delete_document(
    doc_id: UUID = Path(...),
    db: DatabaseService = Depends(get_database_service),
) -> ResponseModel[dict[str, bool]]:
    """Delete a document."""
    ok = await db.delete_document(doc_id)
    if not ok:
        raise HTTPException(status_code=404, detail="document not found")
    return ResponseModel(status=ResponseStatus.SUCCESS, data={"deleted": True})


@router.post("/search", response_model=ResponseModel[List[Document]])
async def search_documents(
    req: SearchRequest, db: DatabaseService = Depends(get_database_service)
) -> ResponseModel[List[Document]]:
    """Vector search for documents."""
    try:
        results = await db.vector_search(req.embedding, req.query)
        return ResponseModel(status=ResponseStatus.SUCCESS, data=results)
    except DatabaseError as exc:
        raise HTTPException(status_code=500, detail="search failed") from exc
