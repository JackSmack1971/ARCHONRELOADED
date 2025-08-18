import pytest
from httpx import ASGITransport, AsyncClient

from src.server import app
from src.server.main import api, connect, disconnect
from src.server.routes import get_database_service


@pytest.mark.asyncio
async def test_health_and_cors() -> None:
    """Health endpoint responds and includes CORS headers."""
    async def _get_db():  # pragma: no cover - simple stub
        class Dummy:
            async def list_projects(self):
                return []

        return Dummy()

    api.dependency_overrides[get_database_service] = _get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/health", headers={"Origin": "http://localhost:3000"})
    api.dependency_overrides.clear()
    assert res.status_code == 200
    assert res.json() == {
        "status": "success",
        "data": {"database": "ok"},
        "error": None,
    }
    assert res.headers["access-control-allow-origin"] == "http://localhost:3000"


@pytest.mark.asyncio
async def test_socket_connection_events() -> None:
    """Socket.IO server connection and disconnection handlers run."""
    await connect("sid", {})
    await disconnect("sid")
