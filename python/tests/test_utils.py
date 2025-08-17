import httpx
import pytest

from src.utils import ExternalServiceError, fetch_with_retry


class MockClient:
    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc_info):
        return False

    async def get(self, url: str):
        return httpx.Response(200, json={"ok": True}, request=httpx.Request("GET", url))


class FailingClient(MockClient):
    async def get(self, url: str):  # type: ignore[override]
        raise httpx.HTTPError("boom")


@pytest.mark.asyncio
async def test_fetch_with_retry(monkeypatch) -> None:
    monkeypatch.setattr(httpx, "AsyncClient", MockClient)
    data = await fetch_with_retry("test")
    assert data == {"ok": True}


@pytest.mark.asyncio
async def test_fetch_with_retry_error(monkeypatch) -> None:
    monkeypatch.setattr(httpx, "AsyncClient", FailingClient)
    with pytest.raises(ExternalServiceError):
        await fetch_with_retry("test")
