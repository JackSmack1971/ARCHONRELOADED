from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Optional
from uuid import UUID
from pydantic import Field, UUID4, field_validator

from .base import TimestampedModel


class ProjectStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Project(TimestampedModel):
    id: UUID4
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: ProjectStatus = ProjectStatus.ACTIVE
    settings: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("id")
    @classmethod
    def validate_uuid4(cls, value: UUID) -> UUID4:
        if value.version != 4:
            raise ValueError("id must be a valid UUID4")
        return UUID4(str(value))
