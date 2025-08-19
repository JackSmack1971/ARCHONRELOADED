import os

import pytest
from httpx import ASGITransport, AsyncClient

os.environ.setdefault("MCP_API_KEY", "test-key")
os.environ.setdefault("SUPABASE_URL", "http://example.com")
os.environ.setdefault("SUPABASE_KEY", "key")

from src.server import api as server_app
from src.mcp.mcp_server import app as mcp_app
from src.agents.main import app as agents_app


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
        await client.get("/health")
        res = await client.get("/metrics")
    assert res.status_code == 200
    body = res.text
    assert "http_requests_total" in body
    assert f'app="{app_name}"' in body
    assert 'path="/health"' in body
