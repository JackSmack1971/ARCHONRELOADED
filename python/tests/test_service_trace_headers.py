import httpx
import pytest
from fastapi import Request

from opentelemetry import propagate, trace
from src.common.service import create_service


@pytest.mark.asyncio
async def test_trace_headers_between_services() -> None:
    captured: dict[str, str | None] = {"trace": None}

    service_b = create_service("service-b")

    @service_b.get("/endpoint")
    async def _endpoint(request: Request) -> dict[str, bool]:
        captured["trace"] = request.headers.get("traceparent")
        return {"ok": True}

    service_a = create_service("service-a")

    @service_a.get("/call")
    async def _call() -> dict[str, bool]:
        headers: dict[str, str] = {}
        propagate.inject(headers)
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=service_b), base_url="http://service-b"
        ) as client:
            await client.get("/endpoint", headers=headers)
        return {"done": True}

    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("root"):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=service_a), base_url="http://service-a"
        ) as client:
            await client.get("/call")

    assert captured["trace"]
    assert len(captured["trace"].split("-")) == 4
