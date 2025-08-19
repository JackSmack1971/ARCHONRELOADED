from __future__ import annotations

"""Shared dependencies for MCP tools."""

from src.server.services.database import DatabaseService
from src.server.services.supabase_client import SupabaseClient


class DependencyInitError(Exception):
    """Raised when dependencies fail to initialize."""


try:
    _client = SupabaseClient()
    db_service = DatabaseService(_client)
except Exception:  # pragma: no cover - initialized lazily when env missing
    db_service = None

__all__ = ["db_service"]
