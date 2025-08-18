"""Core FastAPI application with Socket.IO integration.

This module exposes the ASGI application used by uvicorn. It configures
environment-driven settings, structured logging, CORS, and a basic health
check endpoint. A Socket.IO server is mounted on top of the FastAPI
application to enable real-time features.
"""

from __future__ import annotations

import sys
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import socketio

from .config import settings
from .auth.dependencies import require_role
from .routes import auth, documents, health, projects, sources, search


class HealthCheckError(Exception):
    """Raised when the health check fails."""


# Configure structured JSON logging
logger.remove()
logger.add(sys.stdout, serialize=True)


# Socket.IO server
sio = socketio.AsyncServer(
    async_mode="asgi", cors_allowed_origins=settings.cors_origins
)


# FastAPI application
api = FastAPI()

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


@sio.event
async def connect(sid: str, environ: dict) -> None:
    """Handle a new Socket.IO connection."""
    logger.info("socket connected", sid=sid)


@sio.event
async def disconnect(sid: str) -> None:
    """Handle Socket.IO disconnects."""
    logger.info("socket disconnected", sid=sid)


# Mount Socket.IO on the FastAPI app
socket_app = socketio.ASGIApp(sio, other_asgi_app=api)


# Expose application for uvicorn
app = socket_app
