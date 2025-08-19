"""Core FastAPI application with Socket.IO integration.

This module exposes the ASGI application used by uvicorn. It configures
environment-driven settings, structured logging, CORS, and a basic health
check endpoint. A Socket.IO server is mounted on top of the FastAPI
application to enable real-time features.
"""

from __future__ import annotations

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio

from src.common.logging import logger
from src.common.metrics import setup_metrics, MetricsError

from .config import settings
from .auth.dependencies import require_role
from .routes import auth, documents, health, projects, sources, search
from .socket import sio


class HealthCheckError(Exception):
    """Raised when the health check fails."""


# FastAPI application
api = FastAPI()
logger.info("Server application created")

try:
    setup_metrics(api, "server")
except MetricsError as exc:  # pragma: no cover - defensive
    logger.error("Metrics setup failed", error=str(exc))

api.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def rate_limit() -> None:
    """Placeholder dependency for future rate limiting."""
    return None


api.include_router(health.router, dependencies=[Depends(rate_limit)])
api.include_router(auth.router)
protected = [Depends(rate_limit), Depends(require_role("user"))]
api.include_router(projects.router, dependencies=protected)
api.include_router(sources.router, dependencies=protected)
api.include_router(documents.router, dependencies=protected)
api.include_router(search.router, dependencies=protected)


# Mount Socket.IO on the FastAPI app
socket_app = socketio.ASGIApp(sio, other_asgi_app=api)


# Expose application for uvicorn
app = socket_app
