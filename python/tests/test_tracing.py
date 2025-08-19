import httpx
import pytest
from fastapi import FastAPI, Request
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

@pytest.mark.asyncio
async def test_trace_header_propagation(monkeypatch) -> None:
    app = FastAPI()
    captured: dict[str, str | None] = {"trace": None}

    @app.get("/echo")
    async def _echo(request: Request) -> dict[str, str | None]:
        captured["trace"] = request.headers.get("traceparent")
        return {"ok": "yes"}

    FastAPIInstrumentor().instrument_app(app)
    HTTPXClientInstrumentor().instrument()

    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    original = httpx.AsyncClient

    class LocalClient:
        def __init__(self, *args, **kwargs) -> None:
            timeout = kwargs.get("timeout")
            transport = httpx.ASGITransport(app=app)
            self._client = original(transport=transport, base_url="http://test", timeout=timeout)

        async def __aenter__(self) -> httpx.AsyncClient:
            return await self._client.__aenter__()

        async def __aexit__(self, exc_type, exc, tb) -> None:
            await self._client.__aexit__(exc_type, exc, tb)

    monkeypatch.setattr(httpx, "AsyncClient", LocalClient)
    monkeypatch.setenv("EXTERNAL_API_BASE", "http://test")

    from src.utils import fetch_with_retry

    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("root") as span:
        await fetch_with_retry("echo")

    assert captured["trace"]
    assert len(captured["trace"].split("-")) == 4
