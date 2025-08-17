import pytest
from httpx import ASGITransport, AsyncClient

from src.mcp.main import app


@pytest.mark.asyncio
async def test_execute_ping() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post("/execute", json={"command": "ping"})
    assert res.status_code == 200
    assert res.json()["result"] == "pong"


@pytest.mark.asyncio
async def test_execute_invalid() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post("/execute", json={"command": "bad"})
    assert res.status_code == 400
