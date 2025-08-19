import logging
from typing import Any, Dict, Protocol, Tuple


class SourceRepository(Protocol):
    """Protocol for source data access."""

    async def list_sources(self) -> Tuple[bool, Dict[str, Any]]: ...

    async def delete(self, source_id: str) -> Tuple[bool, Dict[str, Any]]: ...

    async def update(
        self, source_id: str, metadata: Dict[str, Any]
    ) -> Tuple[bool, Dict[str, Any]]: ...


class SourceManagementError(Exception):
    """Custom exception for source management failures."""


class SourceManagementService:
    """Service for managing knowledge sources."""

    def __init__(self, repository: SourceRepository) -> None:
        self._repo = repository
        self._logger = logging.getLogger(__name__)

    async def get_available_sources(self) -> Tuple[bool, Dict[str, Any]]:
        """Return all available sources."""
        try:
            ok, data = await self._repo.list_sources()
            if not ok:
                return False, data
            sources = data.get("sources", [])
            return True, {"sources": sources, "total_count": len(sources)}
        except Exception as exc:
            self._logger.error("get_available_sources failed: %s", exc)
            raise SourceManagementError("failed to fetch sources") from exc

    async def delete_source(self, source_id: str) -> Tuple[bool, Dict[str, Any]]:
        """Delete a source by its identifier."""
        if not source_id:
            return False, {"error": "invalid source id"}
        try:
            ok, data = await self._repo.delete(source_id)
            if ok:
                self._logger.info("Deleted source %s", source_id)
            else:
                self._logger.error(
                    "Failed to delete source %s: %s", source_id, data.get("error")
                )
            return ok, data
        except Exception as exc:
            self._logger.error("delete_source failed: %s", exc)
            raise SourceManagementError("failed to delete source") from exc

    async def update_source_metadata(
        self, source_id: str, metadata: Dict[str, Any]
    ) -> Tuple[bool, Dict[str, Any]]:
        """Update metadata for a given source."""
        if not source_id or not isinstance(metadata, dict) or not metadata:
            return False, {"error": "invalid input"}
        try:
            ok, data = await self._repo.update(source_id, metadata)
            if ok:
                self._logger.info("Updated source %s", source_id)
            else:
                self._logger.error(
                    "Failed to update source %s: %s", source_id, data.get("error")
                )
            return ok, data
        except Exception as exc:
            self._logger.error("update_source_metadata failed: %s", exc)
            raise SourceManagementError("failed to update source") from exc
