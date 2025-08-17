from types import SimpleNamespace
from unittest.mock import patch

import pytest

from src.server.services import SupabaseClient, SupabaseClientError


@pytest.mark.asyncio
async def test_supabase_client_init_and_get(monkeypatch) -> None:
    monkeypatch.setenv("SUPABASE_URL", "http://example.com")
    monkeypatch.setenv("SUPABASE_KEY", "secret")
    monkeypatch.setenv("SUPABASE_TIMEOUT", "5")
    monkeypatch.setenv("SUPABASE_POOL_SIZE", "2")

    async def fake_create(url: str, key: str, opts: object) -> object:
        return SimpleNamespace()

    with patch("src.server.services.supabase_client.create_async_client", fake_create):
        client = SupabaseClient()
        sb = await client.get_client()
        assert sb is not None
        await client.close()


def test_supabase_client_missing_env(monkeypatch) -> None:
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_KEY", raising=False)
    with pytest.raises(SupabaseClientError):
        SupabaseClient()
