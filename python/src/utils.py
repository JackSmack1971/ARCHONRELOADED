from __future__ import annotations

import os
from typing import Any

import httpx
from opentelemetry import propagate, trace
from tenacity import AsyncRetrying, stop_after_attempt, wait_fixed


class ExternalServiceError(Exception):
    """Raised when an external API call fails."""


tracer = trace.get_tracer(__name__)


async def fetch_with_retry(endpoint: str) -> dict[str, Any]:
    """Fetch JSON from an external API with retries and timeout."""
    base_url = os.getenv("EXTERNAL_API_BASE", "https://example.com")
    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    headers: dict[str, str] = {}
    with tracer.start_as_current_span("external.request", {"http.url": url}) as span:
        try:
            async for attempt in AsyncRetrying(
                stop=stop_after_attempt(3), wait=wait_fixed(1)
            ):
                with attempt:
                    async with httpx.AsyncClient(timeout=5.0) as client:
                        propagate.inject(headers)
                        response = await client.get(url, headers=headers)
                        response.raise_for_status()
                        return response.json()
        except Exception as exc:  # pragma: no cover - tenacity error wrapping
            span.record_exception(exc)
            raise ExternalServiceError(str(exc)) from exc
    raise ExternalServiceError(f"Failed to fetch data from {url}")
