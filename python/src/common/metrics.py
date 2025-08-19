from __future__ import annotations

import time
from typing import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from starlette.middleware.base import BaseHTTPMiddleware


class MetricsError(Exception):
    """Raised when metrics operations fail."""


REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["app", "method", "path", "status_code"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["app", "method", "path"],
)


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware collecting Prometheus metrics."""

    def __init__(self, app: FastAPI, app_name: str) -> None:
        super().__init__(app)
        self.app_name = app_name

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start
        try:
            REQUEST_COUNT.labels(
                self.app_name,
                request.method,
                request.url.path,
                str(response.status_code),
            ).inc()
            REQUEST_LATENCY.labels(
                self.app_name, request.method, request.url.path
            ).observe(duration)
        except Exception as exc:  # pragma: no cover - defensive
            raise MetricsError("Failed to record metrics") from exc
        return response


def setup_metrics(app: FastAPI, app_name: str) -> None:
    """Attach metrics middleware and expose /metrics endpoint."""
    try:
        app.add_middleware(MetricsMiddleware, app_name=app_name)  # type: ignore[arg-type]

        @app.get("/metrics")
        async def _metrics() -> Response:  # pragma: no cover - simple wrapper
            return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
    except Exception as exc:  # pragma: no cover - defensive
        raise MetricsError("Failed to set up metrics") from exc
