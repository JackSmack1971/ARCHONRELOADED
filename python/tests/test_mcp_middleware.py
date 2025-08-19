import asyncio
import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from src.server.middleware import MCPMiddleware


@pytest.mark.asyncio
async def test_mcp_request_routed() -> None:
    app = FastAPI()
    async def handler(payload):
        return {"content": "ok"}
    app.add_middleware(MCPMiddleware, handlers={"/mcp": handler}, retries=1)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post("/mcp", headers={"X-MCP-Request": "true"}, json={"action": "ping"})
    assert res.status_code == 200
    assert res.json() == {"content": "ok"}


@pytest.mark.asyncio
async def test_invalid_payload_returns_400() -> None:
    app = FastAPI()
    async def handler(payload):
        return {"content": "ok"}
    app.add_middleware(MCPMiddleware, handlers={"/mcp": handler})
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post("/mcp", headers={"X-MCP-Request": "true"}, json={"bad": "data"})
    assert res.status_code == 400
    assert res.json()["error"] == "missing_action"


@pytest.mark.asyncio
async def test_handler_timeout_retries() -> None:
    app = FastAPI()
    calls = {"count": 0}
    async def handler(payload):
        calls["count"] += 1
        await asyncio.sleep(0.2)
        return {"content": "late"}
    app.add_middleware(MCPMiddleware, handlers={"/mcp": handler}, timeout=0.05, retries=2)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post("/mcp", headers={"X-MCP-Request": "true"}, json={"action": "ping"})
    assert res.status_code == 504
    assert calls["count"] == 2
