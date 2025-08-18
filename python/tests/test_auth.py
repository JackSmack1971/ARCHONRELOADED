import pytest
from httpx import ASGITransport, AsyncClient

from src.server import app
from src.server.main import api
from src.server.routes import get_database_service


class DummyDB:
    async def list_projects(self):
        return []


@pytest.mark.asyncio
async def test_auth_flow() -> None:
    async def _get_db():
        return DummyDB()

    api.dependency_overrides[get_database_service] = _get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post(
            "/auth/register",
            json={"username": "alice", "password": "password123"},
        )
        assert res.status_code == 200

        res = await client.post(
            "/auth/login",
            json={"username": "alice", "password": "password123"},
        )
        token = res.json()["data"]["access_token"]

        unauth = await client.get("/projects/")
        assert unauth.status_code == 403

        client.headers["Authorization"] = f"Bearer {token}"
        authd = await client.get("/projects/")
        assert authd.status_code == 200
    api.dependency_overrides.clear()

