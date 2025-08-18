import io
from typing import Dict
from uuid import uuid4

import pytest

import importlib
import sys
import types
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(PACKAGE_ROOT))

src_pkg = sys.modules.setdefault("src", types.ModuleType("src"))
src_pkg.__path__ = [str(PACKAGE_ROOT)]
server_pkg = types.ModuleType("src.server")
server_pkg.__path__ = [str(PACKAGE_ROOT / "server")]
setattr(src_pkg, "server", server_pkg)
sys.modules["src.server"] = server_pkg
routes_pkg = types.ModuleType("src.server.routes")
routes_pkg.__path__ = [str(PACKAGE_ROOT / "server" / "routes")]
setattr(server_pkg, "routes", routes_pkg)
async def _dummy_get_db():  # pragma: no cover - placeholder
    pass

routes_pkg.get_database_service = _dummy_get_db
sys.modules["src.server.routes"] = routes_pkg
services_pkg = types.ModuleType("src.server.services")
services_pkg.__path__ = []
sys.modules["src.server.services"] = services_pkg
database_module = types.ModuleType("src.server.services.database")


class DatabaseError(Exception):
    pass


class DatabaseService:  # pragma: no cover - placeholder
    pass


database_module.DatabaseError = DatabaseError
database_module.DatabaseService = DatabaseService
sys.modules["src.server.services.database"] = database_module

embedding_module = types.ModuleType("src.server.services.embedding")


async def generate_embedding(text: str):  # pragma: no cover - placeholder
    return []


embedding_module.generate_embedding = generate_embedding
sys.modules["src.server.services.embedding"] = embedding_module

socket_module = types.ModuleType("src.server.socket")


class BroadcastError(Exception):
    pass


async def broadcast_upload_progress(channel: str, message: Dict[str, str]):  # pragma: no cover
    return None


socket_module.BroadcastError = BroadcastError
socket_module.broadcast_upload_progress = broadcast_upload_progress
sys.modules["src.server.socket"] = socket_module

documents = importlib.import_module("src.server.routes.documents")

INGESTION_PROGRESS = documents.INGESTION_PROGRESS
_create_document_entry = documents._create_document_entry
_queue_embedding = documents._queue_embedding
_validate_upload = documents._validate_upload
DocumentCreationError = documents.DocumentCreationError
EmbeddingQueueError = documents.EmbeddingQueueError
UploadValidationError = documents.UploadValidationError
Document = documents.Document
DatabaseError = documents.DatabaseError


class DummyUploadFile:
    def __init__(self, filename: str, data: bytes, content_type: str) -> None:
        self.filename = filename
        self.content_type = content_type
        self.file = io.BytesIO(data)

    async def read(self) -> bytes:  # pragma: no cover - simple read
        return self.file.read()


class DummyDB:
    async def create_document(self, doc: Document) -> Document:  # pragma: no cover - simple store
        self.doc = doc
        return doc


class FailingDB:
    async def create_document(self, doc: Document) -> Document:  # pragma: no cover - always fails
        raise DatabaseError("fail")


class DummyBackground:
    def __init__(self) -> None:
        self.tasks = []

    def add_task(self, func, *args) -> None:  # pragma: no cover - simple record
        self.tasks.append((func, args))


class FailingBackground:
    def add_task(self, func, *args) -> None:  # pragma: no cover - always fails
        raise RuntimeError("fail")


@pytest.mark.asyncio
async def test_validate_upload_success() -> None:
    file = DummyUploadFile("doc.txt", b"hello", "text/plain")
    content = await _validate_upload(file)
    assert content == "hello"


@pytest.mark.asyncio
async def test_validate_upload_bad_type() -> None:
    file = DummyUploadFile("doc.jpg", b"hi", "image/jpeg")
    with pytest.raises(UploadValidationError):
        await _validate_upload(file)


@pytest.mark.asyncio
async def test_create_document_entry() -> None:
    db = DummyDB()
    doc_id, source_id = uuid4(), uuid4()
    doc = await _create_document_entry(doc_id, source_id, "hello", db)
    assert doc.id == doc_id and db.doc is doc


@pytest.mark.asyncio
async def test_create_document_entry_failure() -> None:
    db = FailingDB()
    with pytest.raises(DocumentCreationError):
        await _create_document_entry(uuid4(), uuid4(), "hi", db)


@pytest.mark.asyncio
async def test_queue_embedding(monkeypatch) -> None:
    async def fake_broadcast(channel: str, message: Dict[str, str]) -> None:
        fake_broadcast.called = True

    fake_broadcast.called = False
    monkeypatch.setattr(
        "src.server.routes.documents.broadcast_upload_progress", fake_broadcast
    )
    db = DummyDB()
    bg = DummyBackground()
    doc_id, source_id = uuid4(), uuid4()
    INGESTION_PROGRESS.clear()
    await _queue_embedding(bg, doc_id, "hi", db, source_id)
    assert INGESTION_PROGRESS[doc_id]["status"] == "queued"
    assert fake_broadcast.called is True
    assert bg.tasks and bg.tasks[0][0].__name__ == "_process_embedding"


@pytest.mark.asyncio
async def test_queue_embedding_failure(monkeypatch) -> None:
    async def fake_broadcast(channel: str, message: Dict[str, str]) -> None:
        pass

    monkeypatch.setattr(
        "src.server.routes.documents.broadcast_upload_progress", fake_broadcast
    )
    bg = FailingBackground()
    db = DummyDB()
    INGESTION_PROGRESS.clear()
    with pytest.raises(EmbeddingQueueError):
        await _queue_embedding(bg, uuid4(), "hi", db, uuid4())
