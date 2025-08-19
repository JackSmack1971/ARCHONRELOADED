from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Tuple, TypeVar

T = TypeVar("T", bound=Dict[str, Any])


class RepositoryError(Exception):
    """Base exception for repository errors."""


class BaseRepository(ABC, Generic[T]):
    """Abstract base class defining async CRUD operations."""

    @abstractmethod
    async def create(self, data: T) -> Tuple[bool, Dict[str, Any]]:
        """Insert a new record."""

    @abstractmethod
    async def read(self, item_id: Any) -> Tuple[bool, Dict[str, Any]]:
        """Fetch a record by its identifier."""

    @abstractmethod
    async def update(self, item_id: Any, data: T) -> Tuple[bool, Dict[str, Any]]:
        """Update an existing record."""

    @abstractmethod
    async def delete(self, item_id: Any) -> Tuple[bool, Dict[str, Any]]:
        """Delete a record by its identifier."""
