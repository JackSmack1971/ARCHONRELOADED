from __future__ import annotations

import asyncio
import hashlib
import os
from typing import List

from tenacity import AsyncRetrying, stop_after_attempt, wait_fixed


EMBEDDING_API_KEY = os.getenv("EMBEDDING_API_KEY", "")


class EmbeddingProcessingError(Exception):
    """Base error for embedding processing failures."""


class EmbeddingGenerationError(EmbeddingProcessingError):
    """Raised when embedding generation fails."""


async def _hash_text(text: str) -> List[float]:
    digest = hashlib.sha256(text.encode()).digest()
    return [b / 255 for b in digest[:8]]


async def generate_embedding(text: str) -> List[float]:
    if not text:
        raise EmbeddingProcessingError("text must not be empty")
    async for attempt in AsyncRetrying(stop=stop_after_attempt(3), wait=wait_fixed(1)):
        with attempt:
            try:
                return await asyncio.wait_for(_hash_text(text), timeout=5.0)
            except Exception as exc:  # noqa: BLE001
                raise EmbeddingGenerationError("embedding failed") from exc
