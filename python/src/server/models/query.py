from __future__ import annotations

from typing import Any, Dict
from pydantic import BaseModel, Field


class Query(BaseModel):
    query_text: str = Field(..., min_length=1)
    match_count: int = Field(default=5, ge=1, le=100)
    filters: Dict[str, Any] = Field(default_factory=dict)
    threshold: float = Field(default=0.5, ge=0.0, le=1.0)
