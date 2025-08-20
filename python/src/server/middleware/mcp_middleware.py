"""Middleware for handling MCP requests directly."""

from __future__ import annotations

import asyncio
from json import JSONDecodeError
from typing import Any, Awaitable, Callable, Dict

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.types import ASGIApp


class InvalidMCPPayloadError(Exception):
    """Raised when MCP payload validation fails."""


class MCPServiceError(Exception):
    """Raised when the MCP service call fails."""


Handler = Callable[[Dict[str, Any]], Awaitable[Dict[str, Any]]]


class MCPMiddleware(BaseHTTPMiddleware):
    """Intercepts MCP requests and routes them to handlers."""

    def __init__(
        self,
        app: ASGIApp,
        handlers: Dict[str, Handler],
        *,
        retries: int = 3,
        timeout: float = 5.0,
    ) -> None:
        super().__init__(app)
        self.handlers = handlers
        self.retries = retries
        self.timeout = timeout

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        if not self._is_mcp_request(request):
            return await call_next(request)
        handler = self.handlers.get(request.url.path)
        if handler is None:
            return await call_next(request)
        try:
            payload = await request.json()
        except JSONDecodeError as exc:
            raise InvalidMCPPayloadError("invalid_json") from exc
        try:
            self._validate_payload(payload)
            result = await self._call_handler_with_retry(handler, payload)
            return JSONResponse(result)
        except InvalidMCPPayloadError as exc:
            return JSONResponse({"error": str(exc)}, status_code=400)
        except MCPServiceError as exc:
            return JSONResponse({"error": str(exc)}, status_code=504)

    @staticmethod
    def _is_mcp_request(request: Request) -> bool:
        """Return True if the request targets the MCP middleware."""
        header = request.headers.get("X-MCP-Request", "").lower() == "true"
        ctype = (
            request.headers.get("content-type", "").lower() == "application/mcp+json"
        )
        return header or ctype

    @staticmethod
    def _validate_payload(payload: Any) -> None:
        """Validate MCP payload structure."""
        if not isinstance(payload, dict):
            raise InvalidMCPPayloadError("payload_not_object")
        action = payload.get("action")
        if not isinstance(action, str) or not action:
            raise InvalidMCPPayloadError("missing_action")

    async def _call_handler_with_retry(
        self, handler: Handler, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        for attempt in range(self.retries):
            try:
                return await asyncio.wait_for(handler(payload), timeout=self.timeout)
            except asyncio.TimeoutError as exc:
                if attempt == self.retries - 1:
                    raise MCPServiceError("timeout") from exc
                await asyncio.sleep(2**attempt)
            except Exception as exc:
                raise MCPServiceError("handler_error") from exc
        raise MCPServiceError("unreachable")
