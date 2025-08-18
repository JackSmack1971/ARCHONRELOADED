import pytest
import asyncio
from uuid import UUID, uuid4

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from src.server import app
from src.server.main import api
from src.server.routes import get_database_service
from src.server.services.database import DatabaseService
from src.server.models.project import Project, ProjectStatus
from src.server.models.source import Source, SourceStatus, SourceType
from src.server.models.document import Document
from src.server.models.query import Query
from src.server.routes.documents import MAX_FILE_SIZE


class FakeDB:
    def __init__(self) -> None:
        self.projects = {}
        self.sources = {}
        self.documents = {}
        self.embeddings = {}

    async def create_project(self, project: Project) -> Project:
        self.projects[project.id] = project
        return project

    async def list_projects(self):
        return list(self.projects.values())

    async def get_project(self, pid):
        return self.projects.get(pid)

    async def update_project(self, pid, data):
        proj = self.projects.get(pid)
        if not proj:
            return None
        new_data = proj.model_dump()
        new_data.update(data)
        proj = Project(**new_data)
        self.projects[pid] = proj
        return proj

    async def delete_project(self, pid):
        return self.projects.pop(pid, None) is not None

    async def create_source(self, source: Source) -> Source:
        self.sources[source.id] = source
        return source

    async def list_sources(self, project_id):
        return [s for s in self.sources.values() if s.project_id == project_id]

    async def get_source(self, sid):
        return self.sources.get(sid)

    async def update_source(self, sid, data):
        src = self.sources.get(sid)
        if not src:
            return None
        new_data = src.model_dump()
        new_data.update(data)
        src = Source(**new_data)
        self.sources[sid] = src
        return src

    async def delete_source(self, sid):
        return self.sources.pop(sid, None) is not None

    async def create_document(self, doc: Document) -> Document:
        self.documents[doc.id] = doc
        return doc

    async def get_document(self, did):
        return self.documents.get(did)

    async def update_document(self, did, data):
        doc = self.documents.get(did)
        if not doc:
            return None
        new_data = doc.model_dump()
        new_data.update(data)
        doc = Document(**new_data)
        self.documents[did] = doc
        return doc

    async def delete_document(self, did):
        return self.documents.pop(did, None) is not None

    async def vector_search(self, embedding, query: Query):
        return list(self.documents.values())[: query.match_count]

    async def store_embedding(self, doc_id, embedding):
        self.embeddings[doc_id] = embedding
        doc = self.documents.get(doc_id)
        if doc:
            new_data = doc.model_dump()
            new_data["embeddings"] = embedding
            self.documents[doc_id] = Document(**new_data)
        return True


@pytest_asyncio.fixture
async def client():
    fake_db = FakeDB()

    async def _get_db():
        return fake_db

    api.dependency_overrides[get_database_service] = _get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post(
            "/auth/register",
            json={"username": "tester", "password": "testpassword123"},
        )
        res = await client.post(
            "/auth/login",
            json={"username": "tester", "password": "testpassword123"},
        )
        token = res.json()["data"]["access_token"]
        client.headers.update({"Authorization": f"Bearer {token}"})
        client.fake_db = fake_db
        yield client
    api.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_project_crud_flow(client: AsyncClient) -> None:
    pid = uuid4()
    proj = {
        "id": str(pid),
        "name": "proj",
        "description": "d",
        "status": ProjectStatus.ACTIVE,
        "settings": {},
    }
    res = await client.post("/projects/", json=proj)
    assert res.status_code == 201
    res = await client.get("/projects/")
    assert res.json()["data"][0]["id"] == str(pid)
    res = await client.put(f"/projects/{pid}", json={"name": "p2"})
    assert res.json()["data"]["name"] == "p2"
    res = await client.delete(f"/projects/{pid}")
    assert res.json()["data"]["deleted"] is True


@pytest.mark.asyncio
async def test_source_crud_flow(client: AsyncClient) -> None:
    pid = uuid4()
    sid = uuid4()
    proj = {
        "id": str(pid),
        "name": "proj",
        "description": "d",
        "status": ProjectStatus.ACTIVE,
        "settings": {},
    }
    await client.post("/projects/", json=proj)
    source = {
        "id": str(sid),
        "project_id": str(pid),
        "type": SourceType.WEB,
        "url": "https://example.com",
        "metadata": {},
        "status": SourceStatus.PENDING,
    }
    res = await client.post("/sources/", json=source)
    assert res.status_code == 201
    res = await client.get(f"/sources/project/{pid}")
    assert res.json()["data"][0]["id"] == str(sid)
    res = await client.put(f"/sources/{sid}", json={"status": SourceStatus.READY})
    assert res.json()["data"]["status"] == SourceStatus.READY
    res = await client.delete(f"/sources/{sid}")
    assert res.json()["data"]["deleted"] is True


@pytest.mark.asyncio
async def test_document_crud_and_search(client: AsyncClient) -> None:
    pid, sid, did = uuid4(), uuid4(), uuid4()
    proj = {
        "id": str(pid),
        "name": "proj",
        "description": "d",
        "status": ProjectStatus.ACTIVE,
        "settings": {},
    }
    await client.post("/projects/", json=proj)
    source = {
        "id": str(sid),
        "project_id": str(pid),
        "type": SourceType.WEB,
        "url": "https://example.com",
        "metadata": {},
        "status": SourceStatus.PENDING,
    }
    await client.post("/sources/", json=source)
    doc = {
        "id": str(did),
        "source_id": str(sid),
        "content": "hello",
        "embeddings": [0.1, 0.2],
        "metadata": {},
    }
    res = await client.post("/documents/", json=doc)
    assert res.status_code == 201
    res = await client.get(f"/documents/{did}")
    assert res.json()["data"]["content"] == "hello"
    res = await client.put(f"/documents/{did}", json={"content": "hi"})
    assert res.json()["data"]["content"] == "hi"
    search_req = {
        "embedding": [0.1, 0.2],
        "query": {"query_text": "hello", "match_count": 5, "filters": {}, "threshold": 0.5},
    }
    res = await client.post("/documents/search", json=search_req)
    assert res.json()["data"][0]["id"] == str(did)
    res = await client.delete(f"/documents/{did}")
    assert res.json()["data"]["deleted"] is True


@pytest.mark.asyncio
async def test_get_database_service_lifecycle(monkeypatch) -> None:
    monkeypatch.setenv("SUPABASE_URL", "http://example.com")
    monkeypatch.setenv("SUPABASE_KEY", "key")
    agen = get_database_service()
    service = await agen.__anext__()
    assert isinstance(service, DatabaseService)
    await agen.aclose()


@pytest.mark.asyncio
async def test_upload_and_search_flow(client: AsyncClient) -> None:
    sid = uuid4()
    files = {"file": ("doc.txt", b"hello world", "text/plain")}
    data = {"source_id": str(sid)}
    res = await client.post("/documents/upload", data=data, files=files)
    assert res.status_code == 202
    doc_id = res.json()["data"]["id"]
    for _ in range(5):
        await asyncio.sleep(0.1)
        status_res = await client.get(f"/documents/status/{doc_id}")
        if status_res.json()["data"]["status"] == "completed":
            break
    assert status_res.json()["data"]["status"] == "completed"
    assert UUID(doc_id) in client.fake_db.embeddings
    query = {
        "query_text": "hello world",
        "match_count": 5,
        "filters": {},
        "threshold": 0.5,
    }
    res = await client.post("/search", json=query)
    assert res.status_code == 200
    assert res.json()["data"][0]["id"] == doc_id


@pytest.mark.asyncio
async def test_upload_rejects_large_file(client: AsyncClient) -> None:
    data = {"source_id": str(uuid4())}
    big_content = b"x" * (MAX_FILE_SIZE + 1)
    files = {"file": ("big.txt", big_content, "text/plain")}
    res = await client.post("/documents/upload", data=data, files=files)
    assert res.status_code == 400
    assert res.json()["detail"] == "file too large"


@pytest.mark.asyncio
async def test_upload_rejects_malformed_pdf(client: AsyncClient) -> None:
    data = {"source_id": str(uuid4())}
    files = {"file": ("bad.pdf", b"not a pdf", "application/pdf")}
    res = await client.post("/documents/upload", data=data, files=files)
    assert res.status_code == 400
    assert res.json()["detail"] == "invalid PDF"


@pytest.mark.asyncio
async def test_process_embedding_handles_expected_error(monkeypatch) -> None:
    from src.server.routes import documents
    from src.server.services.embedding import EmbeddingProcessingError

    async def fake_generate(_: str):
        raise EmbeddingProcessingError("boom")

    async def fake_broadcast(*_args, **_kwargs):
        return None

    monkeypatch.setattr(documents, "generate_embedding", fake_generate)
    monkeypatch.setattr(documents, "broadcast_upload_progress", fake_broadcast)

    doc_id, project_id = uuid4(), uuid4()
    documents.INGESTION_PROGRESS[doc_id] = {"status": "pending"}
    await documents._process_embedding(doc_id, "content", FakeDB(), project_id)

    assert documents.INGESTION_PROGRESS[doc_id]["status"] == "failed"
    assert documents.INGESTION_PROGRESS[doc_id]["error"] == "boom"


@pytest.mark.asyncio
async def test_process_embedding_propagates_unexpected_exceptions(monkeypatch) -> None:
    from src.server.routes import documents

    async def fake_generate(_: str):
        return [0.1]

    async def fake_broadcast(*_args, **_kwargs):
        return None

    fake_db = FakeDB()

    async def bad_store(*_args, **_kwargs):
        raise RuntimeError("db down")

    monkeypatch.setattr(documents, "generate_embedding", fake_generate)
    monkeypatch.setattr(documents, "broadcast_upload_progress", fake_broadcast)
    monkeypatch.setattr(fake_db, "store_embedding", bad_store)

    doc_id, project_id = uuid4(), uuid4()
    documents.INGESTION_PROGRESS[doc_id] = {"status": "pending"}

    with pytest.raises(RuntimeError):
        await documents._process_embedding(doc_id, "content", fake_db, project_id)

    assert documents.INGESTION_PROGRESS[doc_id]["status"] == "processing"
