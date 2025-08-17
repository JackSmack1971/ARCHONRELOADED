import pytest
from httpx import ASGITransport, AsyncClient

from src.common.service import create_service
from src.utils import ExternalServiceError


@pytest.mark.asyncio
async def test_create_service_health() -> None:
    app = create_service()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_error_handler() -> None:
    app = create_service()

    @app.get("/boom")
    async def boom() -> None:
        raise ExternalServiceError("fail")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/boom")
    assert res.status_code == 502
    assert res.json()["detail"] == "fail"
