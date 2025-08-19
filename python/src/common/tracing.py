from __future__ import annotations

import os

from fastapi import FastAPI
from opentelemetry import trace, propagate
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


class TracingSetupError(Exception):
    """Raised when OpenTelemetry setup fails."""


def setup_tracing(service_name: str, app: FastAPI | None = None) -> None:
    """Configure OpenTelemetry tracing for a service.

    Args:
        service_name: Name of the service for trace grouping.
        app: Optional FastAPI application to instrument.
    """
    try:
        endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
        resource = Resource.create({"service.name": service_name})
        provider = trace.get_tracer_provider()
        if not isinstance(provider, TracerProvider):
            provider = TracerProvider(resource=resource)
            exporter = OTLPSpanExporter(endpoint=endpoint, insecure=True)
            provider.add_span_processor(BatchSpanProcessor(exporter))
            trace.set_tracer_provider(provider)
        HTTPXClientInstrumentor().instrument()
        if app:
            FastAPIInstrumentor().instrument_app(app)
        propagate.set_global_textmap(propagate.get_global_textmap())
    except Exception as exc:  # pragma: no cover - defensive
        raise TracingSetupError("Tracing initialization failed") from exc
