import pytest
from httpx import ASGITransport, AsyncClient

from src.server.main import app


@pytest.mark.asyncio
async def test_health() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_process(monkeypatch) -> None:
    async def mock_fetch(endpoint: str):
        return {"url": "mock://"}

    monkeypatch.setattr("src.server.main.fetch_with_retry", mock_fetch)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post("/process", json={"text": "hi"})
    assert res.status_code == 200
    assert res.json()["echo"] == "hi"
