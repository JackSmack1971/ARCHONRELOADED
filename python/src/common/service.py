from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.utils import ExternalServiceError


async def _health() -> dict[str, str]:
    """Simple health check endpoint."""
    return {"status": "ok"}


def create_service() -> FastAPI:
    """Create a FastAPI app with health and error handlers."""
    app = FastAPI()
    app.get("/health")(_health)

    @app.exception_handler(ExternalServiceError)
    async def _handle_external(_: Request, exc: ExternalServiceError) -> JSONResponse:
        return JSONResponse(status_code=502, content={"detail": str(exc)})

    @app.exception_handler(Exception)
    async def _handle_general(_: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(status_code=500, content={"detail": str(exc)})

    return app
