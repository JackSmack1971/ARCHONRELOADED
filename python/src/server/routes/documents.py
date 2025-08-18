"""Document routes including upload and ingestion progress."""

from __future__ import annotations

import io
from uuid import UUID, uuid4
from typing import Any, Dict, List, Optional

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    HTTPException,
    Path,
    UploadFile,
    Form,
    status,
)
from pydantic import BaseModel, UUID4
from PyPDF2 import PdfReader

from ..models.base import ResponseModel, ResponseStatus
from ..models.document import Document
from ..models.query import Query
from ..services.database import DatabaseError, DatabaseService
from ..services.embedding import (
    EmbeddingProcessingError,
    generate_embedding,
)
from ..socket import broadcast_upload_progress, BroadcastError
from . import get_database_service
from loguru import logger


MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


class FileProcessingError(Exception):
    """Raised when an uploaded file cannot be processed."""


class UploadValidationError(Exception):
    """Raised when an upload is invalid."""


class DocumentCreationError(Exception):
    """Raised when document creation fails."""


class EmbeddingQueueError(Exception):
    """Raised when queuing embedding generation fails."""


class DocumentUpdate(BaseModel):
    content: Optional[str] = None
    embeddings: Optional[List[float]] = None
    metadata: Optional[Dict[str, Any]] = None


class SearchRequest(BaseModel):
    embedding: List[float]
    query: Query


router = APIRouter(prefix="/documents", tags=["documents"])


INGESTION_PROGRESS: Dict[UUID, Dict[str, str]] = {}


async def _read_file(file: UploadFile) -> str:
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)
    if size > MAX_FILE_SIZE:
        raise FileProcessingError("file too large")
    try:
        data = await file.read()
    except Exception as exc:  # noqa: BLE001
        raise FileProcessingError("unable to read file") from exc

    if file.content_type == "application/pdf":
        try:
            reader = PdfReader(io.BytesIO(data))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as exc:  # noqa: BLE001
            raise FileProcessingError("invalid PDF") from exc

    try:
        return data.decode()
    except Exception as exc:  # noqa: BLE001
        raise FileProcessingError("invalid text") from exc


async def _validate_upload(file: UploadFile) -> str:
    """Validate uploaded file and return its content."""
    if file.content_type not in {"text/plain", "application/pdf"}:
        raise UploadValidationError("unsupported file type")
    try:
        return await _read_file(file)
    except FileProcessingError as exc:
        raise UploadValidationError(str(exc)) from exc


async def _create_document_entry(
    doc_id: UUID, source_id: UUID4, content: str, db: DatabaseService
) -> Document:
    """Store a new document in the database."""
    doc = Document(
        id=doc_id, source_id=source_id, content=content, embeddings=[], metadata={}
    )
    try:
        return await db.create_document(doc)
    except DatabaseError as exc:
        raise DocumentCreationError("database create failed") from exc


async def _process_embedding(
    doc_id: UUID, content: str, db: DatabaseService, source_id: UUID4
) -> None:
    INGESTION_PROGRESS[doc_id]["status"] = "processing"
    try:
        await broadcast_upload_progress(
            str(source_id), {"doc_id": str(doc_id), "status": "processing"}
        )
    except BroadcastError:
        logger.warning("upload progress broadcast failed", doc_id=str(doc_id))
    try:
        emb = await generate_embedding(content)
        await db.store_embedding(doc_id, emb)
        await db.update_document(doc_id, {"embeddings": emb})
        INGESTION_PROGRESS[doc_id]["status"] = "completed"
        try:
            await broadcast_upload_progress(
                str(source_id), {"doc_id": str(doc_id), "status": "completed"}
            )
        except BroadcastError:
            logger.warning("upload progress broadcast failed", doc_id=str(doc_id))
    except EmbeddingProcessingError as exc:
        INGESTION_PROGRESS[doc_id] = {"status": "failed", "error": str(exc)}
        try:
            await broadcast_upload_progress(
                str(source_id),
                {"doc_id": str(doc_id), "status": "failed", "error": str(exc)},
            )
        except BroadcastError:
            logger.warning("upload progress broadcast failed", doc_id=str(doc_id))


async def _queue_embedding(
    background: BackgroundTasks,
    doc_id: UUID,
    content: str,
    db: DatabaseService,
    source_id: UUID4,
) -> None:
    """Queue embedding generation and broadcast status."""
    INGESTION_PROGRESS[doc_id] = {"status": "queued"}
    try:
        await broadcast_upload_progress(
            str(source_id), {"doc_id": str(doc_id), "status": "queued"}
        )
    except BroadcastError:
        logger.warning("upload progress broadcast failed", doc_id=str(doc_id))
    try:
        background.add_task(_process_embedding, doc_id, content, db, source_id)
    except Exception as exc:  # noqa: BLE001
        raise EmbeddingQueueError("failed to queue embedding") from exc


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


@router.post("/upload", response_model=ResponseModel[Dict[str, UUID]], status_code=status.HTTP_202_ACCEPTED)
async def upload_document(
    background: BackgroundTasks,
    source_id: UUID4 = Form(...),
    file: UploadFile = File(...),
    db: DatabaseService = Depends(get_database_service),
) -> ResponseModel[Dict[str, UUID]]:
    try:
        content = await _validate_upload(file)
        doc_id = uuid4()
        doc = await _create_document_entry(doc_id, source_id, content, db)
        await _queue_embedding(background, doc_id, content, db, source_id)
        return ResponseModel(status=ResponseStatus.SUCCESS, data={"id": doc.id})
    except UploadValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except DocumentCreationError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except EmbeddingQueueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="upload failed") from exc


@router.get("/status/{doc_id}", response_model=ResponseModel[Dict[str, str]])
async def ingestion_status(doc_id: UUID) -> ResponseModel[Dict[str, str]]:
    status_info = INGESTION_PROGRESS.get(doc_id)
    if not status_info:
        raise HTTPException(status_code=404, detail="document not found")
    return ResponseModel(status=ResponseStatus.SUCCESS, data=status_info)
