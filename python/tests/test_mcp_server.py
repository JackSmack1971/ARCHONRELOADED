import os
from typing import Set
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient

# Configure environment before importing app
os.environ["MCP_API_KEY"] = "test-key"
os.environ["SUPABASE_URL"] = "http://example.com"
os.environ["SUPABASE_KEY"] = "key"

from src.mcp.mcp_server import app  # noqa: E402
from src.mcp import deps  # noqa: E402
from src.server.models.document import Document  # noqa: E402
from src.server.models.project import Project  # noqa: E402


class FakeDatabaseService:
    """In-memory stand-in for the real database."""

    def __init__(self) -> None:
        self.projects: dict[str, Project] = {}
        self.documents: dict[str, Document] = {}

    async def create_project(self, project: Project) -> Project:
        self.projects[str(project.id)] = project
        return project

    async def list_projects(self) -> list[Project]:
        return list(self.projects.values())

    async def get_project(self, project_id):
        return self.projects.get(str(project_id))

    async def vector_search(self, embedding, query):
        return list(self.documents.values())[: query.match_count]

    async def get_document(self, doc_id):
        return self.documents.get(str(doc_id))


fake_db = FakeDatabaseService()
deps.db_service = fake_db


@pytest.mark.asyncio
async def test_sse_connect() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        headers = {"Authorization": "Bearer test-key"}
        res = await client.get("/sse?client_id=abc&close=1", headers=headers)
        assert res.status_code == 200
        assert res.headers["content-type"].startswith("text/event-stream")
        assert res.text.startswith("data: connected")


@pytest.mark.asyncio
async def test_tool_workflow() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        headers = {"Authorization": "Bearer test-key"}
        # list tools
        res = await client.post(
            "/rpc", headers=headers, json={"id": "1", "method": "tools/list"}
        )
        tools: Set[str] = set(res.json()["result"]["tools"])
        assert {
            "create_project",
            "list_projects",
            "get_project_status",
            "search_documents",
            "get_document",
            "create_task",
            "get_task_status",
        } <= tools
        # create project
        res = await client.post(
            "/rpc",
            headers=headers,
            json={"id": "2", "method": "create_project", "params": {"name": "demo"}},
        )
        project_id = res.json()["result"]["id"]
        # list projects
        res = await client.post(
            "/rpc",
            headers=headers,
            json={"id": "3", "method": "list_projects"},
        )
        assert res.json()["result"]["projects"][0]["id"] == project_id
        # prepare document and test search & retrieval
        doc_id = uuid4()
        fake_db.documents[str(doc_id)] = Document(
            id=doc_id, source_id=uuid4(), content="hello", embeddings=[], metadata={}
        )
        res = await client.post(
            "/rpc",
            headers=headers,
            json={"id": "4", "method": "search_documents", "params": {"query": "hi"}},
        )
        assert res.json()["result"]["documents"]
        res = await client.post(
            "/rpc",
            headers=headers,
            json={"id": "5", "method": "get_document", "params": {"document_id": str(doc_id)}},
        )
        assert res.json()["result"]["id"] == str(doc_id)
        # task creation and status
        res = await client.post(
            "/rpc",
            headers=headers,
            json={
                "id": "6",
                "method": "create_task",
                "params": {"project_id": project_id, "description": "work"},
            },
        )
        task_id = res.json()["result"]["id"]
        res = await client.post(
            "/rpc",
            headers=headers,
            json={"id": "7", "method": "get_task_status", "params": {"task_id": task_id}},
        )
        assert res.json()["result"]["status"] == "pending"


@pytest.mark.asyncio
async def test_auth_required() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post("/rpc", json={"id": "1", "method": "tools/list"})
    assert res.status_code == 401
