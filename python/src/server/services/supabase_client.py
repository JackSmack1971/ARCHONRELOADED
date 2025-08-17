from __future__ import annotations

import os
from typing import Optional

import httpx
from supabase import AsyncClient, AsyncClientOptions, create_async_client
from tenacity import AsyncRetrying, retry_if_exception_type, stop_after_attempt, wait_exponential


class SupabaseClientError(Exception):
    """Raised when the Supabase client fails to initialize or connect."""


class SupabaseClient:
    """Asynchronous Supabase client with connection pooling and retries."""

    def __init__(self) -> None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if not url or not key:
            raise SupabaseClientError("Supabase credentials missing")
        timeout = int(os.getenv("SUPABASE_TIMEOUT", "10"))
        pool = int(os.getenv("SUPABASE_POOL_SIZE", "10"))
        self._url = url
        self._key = key
        self._session = httpx.AsyncClient(
            timeout=timeout, limits=httpx.Limits(max_connections=pool)
        )
        self._client: Optional[AsyncClient] = None

    async def get_client(self) -> AsyncClient:
        """Get or create a connected Supabase client with retry logic."""
        if self._client is not None:
            return self._client
        async for attempt in AsyncRetrying(
            retry=retry_if_exception_type(httpx.HTTPError),
            stop=stop_after_attempt(3),
            wait=wait_exponential(min=1, max=4),
        ):
            with attempt:
                opts = AsyncClientOptions(httpx_client=self._session)
                self._client = await create_async_client(self._url, self._key, opts)
        return self._client

    async def close(self) -> None:
        """Close the underlying HTTP session."""
        await self._session.aclose()
