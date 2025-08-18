"""FastAPI route dependencies and exports."""
from __future__ import annotations

from collections.abc import AsyncGenerator
from fastapi import Depends

from ..services.database import DatabaseService
from ..services.supabase_client import SupabaseClient


async def get_database_service() -> AsyncGenerator[DatabaseService, None]:
    """Provide a DatabaseService instance per request."""
    client = SupabaseClient()
    service = DatabaseService(client)
    try:
        yield service
    finally:
        await client.close()


__all__ = ["get_database_service"]
