import pytest
from httpx import ASGITransport, AsyncClient

from src.server import api as server_app
from src.common.service import create_service

mcp_app = create_service("mcp")
agents_app = create_service("agents")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "app, app_name",
    [
        (server_app, "server"),
        (mcp_app, "mcp"),
        (agents_app, "agents"),
    ],
)
async def test_metrics_endpoint(app, app_name) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.get("/metrics/")
        res = await client.get("/metrics/")
    assert res.status_code == 200
    body = res.text
    assert "http_requests_total" in body
    assert f'app="{app_name}"' in body
    assert 'path="/metrics/"' in body
