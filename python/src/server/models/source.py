from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Optional
from uuid import UUID
from pydantic import Field, HttpUrl, UUID4, field_validator

from .base import TimestampedModel


class SourceType(str, Enum):
    WEB = "web"
    FILE = "file"
    OTHER = "other"


class SourceStatus(str, Enum):
    PENDING = "pending"
    READY = "ready"
    FAILED = "failed"


class Source(TimestampedModel):
    id: UUID4
    project_id: UUID4
    type: SourceType
    url: HttpUrl
    metadata: Dict[str, Any] = Field(default_factory=dict)
    status: SourceStatus = SourceStatus.PENDING

    @field_validator("id", "project_id")
    @classmethod
    def validate_uuid4(cls, value: UUID) -> UUID4:
        if value.version != 4:
            raise ValueError("must be a valid UUID4")
        return UUID4(str(value))
