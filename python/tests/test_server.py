import pytest
from httpx import ASGITransport, AsyncClient

from src.server import app
from src.server.main import connect, disconnect


@pytest.mark.asyncio
async def test_health_and_cors() -> None:
    """Health endpoint responds and includes CORS headers."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/health", headers={"Origin": "http://localhost:3000"})
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}
    assert res.headers["access-control-allow-origin"] == "http://localhost:3000"


@pytest.mark.asyncio
async def test_socket_connection_events() -> None:
    """Socket.IO server connection and disconnection handlers run."""
    await connect("sid", {})
    await disconnect("sid")
