import os
from typing import Set

import asyncio
import pytest
from httpx import ASGITransport, AsyncClient

# Set API key before importing the app
os.environ["MCP_API_KEY"] = "test-key"
from src.mcp.mcp_server import app  # noqa: E402
from src.mcp.tools.project_tools import PROJECTS  # noqa: E402
from src.mcp.tools.source_tools import PROJECT_SOURCES  # noqa: E402


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
    PROJECTS.clear()
    PROJECT_SOURCES.clear()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        headers = {"Authorization": "Bearer test-key"}
        res = await client.post(
            "/rpc", headers=headers, json={"id": "1", "method": "tools/list"}
        )
        tools: Set[str] = set(res.json()["result"]["tools"])
        assert {
            "list_projects",
            "create_project",
            "get_project_status",
            "add_source",
            "query_knowledge",
        } <= tools
        res = await client.post(
            "/rpc",
            headers=headers,
            json={"id": "2", "method": "create_project", "params": {"name": "demo"}},
        )
        project_id = res.json()["result"]["id"]
        res = await client.post(
            "/rpc",
            headers=headers,
            json={
                "id": "3",
                "method": "add_source",
                "params": {"project_id": project_id, "source": "doc"},
            },
        )
        assert "doc" in res.json()["result"]["sources"]
        res = await client.post(
            "/rpc",
            headers=headers,
            json={
                "id": "4",
                "method": "query_knowledge",
                "params": {"project_id": project_id, "query": "doc"},
            },
        )
        assert res.json()["result"]["matches"] == ["doc"]
        res = await client.post(
            "/rpc",
            headers=headers,
            json={
                "id": "5",
                "method": "get_project_status",
                "params": {"project_id": project_id},
            },
        )
        assert res.json()["result"]["name"] == "demo"


@pytest.mark.asyncio
async def test_auth_required() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post("/rpc", json={"id": "1", "method": "tools/list"})
    assert res.status_code == 401
