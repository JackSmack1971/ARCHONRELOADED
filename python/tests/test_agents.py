import pytest
from httpx import ASGITransport, AsyncClient

from src.agents.main import app
from src.common import logging as log_module


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
async def test_run_invalid() -> None:
    transport = ASGITransport(app=app)
    called: dict[str, str] = {}

    async def fake_log_error(message: str, **data):
        called["message"] = message

    # Patch logging to capture error log
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(log_module, "log_error", fake_log_error)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post("/run", json={"task": "bad"})
    assert res.status_code == 400
    assert called["message"] == "Unsupported task"
    monkeypatch.undo()
