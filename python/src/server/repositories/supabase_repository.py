from __future__ import annotations

from typing import Any, Dict, Generic, Tuple, TypeVar

import httpx
from supabase import AsyncClient
from tenacity import (
    AsyncRetrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from .base_repository import BaseRepository, RepositoryError

T = TypeVar("T", bound=Dict[str, Any])


class SupabaseRepositoryError(RepositoryError):
    """Raised when Supabase operations fail."""


class SupabaseRepository(BaseRepository[T], Generic[T]):
    """Supabase implementation of the repository pattern."""

    def __init__(self, client: AsyncClient, table: str) -> None:
        if not table:
            raise SupabaseRepositoryError("table name required")
        self._client = client
        self._table = table

    async def _execute(self, builder: Any) -> Tuple[bool, Dict[str, Any]]:
        try:
            async for attempt in AsyncRetrying(
                retry=retry_if_exception_type(httpx.HTTPError),
                stop=stop_after_attempt(3),
                wait=wait_exponential(min=1, max=4),
            ):
                with attempt:
                    response = await builder.execute()
                    return True, response.data
        except Exception as exc:
            return False, {"error": str(exc)}

    async def create(self, data: T) -> Tuple[bool, Dict[str, Any]]:
        if not isinstance(data, dict) or not data:
            raise SupabaseRepositoryError("invalid data")
        builder = self._client.table(self._table).insert(data)
        return await self._execute(builder)

    async def read(self, item_id: Any) -> Tuple[bool, Dict[str, Any]]:
        if not item_id:
            raise SupabaseRepositoryError("invalid id")
        builder = self._client.table(self._table).select("*").eq("id", item_id).single()
        return await self._execute(builder)

    async def update(self, item_id: Any, data: T) -> Tuple[bool, Dict[str, Any]]:
        if not item_id:
            raise SupabaseRepositoryError("invalid id")
        if not isinstance(data, dict) or not data:
            raise SupabaseRepositoryError("invalid data")
        builder = (
            self._client.table(self._table).update(data).eq("id", item_id).single()
        )
        return await self._execute(builder)

    async def delete(self, item_id: Any) -> Tuple[bool, Dict[str, Any]]:
        if not item_id:
            raise SupabaseRepositoryError("invalid id")
        builder = self._client.table(self._table).delete().eq("id", item_id).single()
        return await self._execute(builder)
