"""Core FastAPI application with Socket.IO integration.

This module exposes the ASGI application used by uvicorn. It configures
environment-driven settings, structured logging, CORS, and a basic health
check endpoint. A Socket.IO server is mounted on top of the FastAPI
application to enable real-time features.
"""

from __future__ import annotations

import sys
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import socketio

from .config import settings


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


@api.get("/health")
async def health(_: None = Depends(rate_limit)) -> dict[str, str]:
    """Simple health check endpoint."""
    try:
        return {"status": "ok"}
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("health check failed")
        raise HTTPException(status_code=503, detail="unhealthy") from exc


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
