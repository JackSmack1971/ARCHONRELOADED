from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Generic, Optional, TypeVar
from pydantic import BaseModel, Field, field_validator, model_validator

T = TypeVar("T")


class TimestampedModel(BaseModel):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("created_at", "updated_at")
    @classmethod
    def ensure_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("timestamp must be timezone-aware")
        return value


class ResponseStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"


class ResponseModel(BaseModel, Generic[T]):
    status: ResponseStatus
    data: Optional[T] = None
    error: Optional[str] = None

    @model_validator(mode="after")
    def validate_error(self) -> "ResponseModel[T]":
        if self.status is ResponseStatus.ERROR and not self.error:
            raise ValueError("error message required when status is ERROR")
        return self
