from __future__ import annotations

from typing import Any, Dict, List
from uuid import UUID
from pydantic import Field, UUID4, field_validator

from .base import TimestampedModel


class Document(TimestampedModel):
    id: UUID4
    source_id: UUID4
    content: str
    embeddings: List[float] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("id", "source_id")
    @classmethod
    def validate_uuid4(cls, value: UUID) -> UUID4:
        if value.version != 4:
            raise ValueError("must be a valid UUID4")
        return UUID4(str(value))
