import pytest
from httpx import ASGITransport, AsyncClient

from src.agents.main import app


@pytest.mark.asyncio
async def test_health() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_run_compute() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post("/run", json={"task": "compute"})
    assert res.status_code == 200
    assert res.json()["status"] == "completed"


@pytest.mark.asyncio
async def test_run_invalid(monkeypatch: pytest.MonkeyPatch) -> None:
    transport = ASGITransport(app=app)
    called: list[str] = []

    async def fake_log_error(message: str, **data):
        called.append(message)

    # Patch logging to capture error log
    monkeypatch.setattr("src.agents.main.log_error", fake_log_error)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post("/run", json={"task": "bad"})
    assert res.status_code == 400
    assert called[0] == "Unsupported task"
