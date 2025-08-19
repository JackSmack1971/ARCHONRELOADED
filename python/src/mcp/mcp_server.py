"""HTTP MCP server with SSE transport."""

from __future__ import annotations

import os
import time
from typing import Any, Dict

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from src.common.logging import logger, log_info
from src.common.service import create_service

from . import ToolExecutionError
from .tools import TOOLS
from .transport.sse import SSETransport

class ConfigurationError(Exception):
    """Raised when required configuration is missing."""


API_KEY = os.getenv("MCP_API_KEY", "")
if not API_KEY:
    raise ConfigurationError("MCP_API_KEY environment variable is required")

RATE_LIMIT: Dict[str, list[float]] = {}
MAX_REQUESTS = 10
WINDOW_SECONDS = 60.0


class AuthenticationError(Exception):
    """Raised when authentication fails."""


class RateLimitError(Exception):
    """Raised when rate limit is exceeded."""


app = create_service("mcp")
transport = SSETransport()


@app.exception_handler(AuthenticationError)
async def _auth_error(_: Request, exc: AuthenticationError) -> JSONResponse:
    return JSONResponse(status_code=401, content={"detail": str(exc)})


@app.exception_handler(RateLimitError)
async def _limit_error(_: Request, exc: RateLimitError) -> JSONResponse:
    return JSONResponse(status_code=429, content={"detail": str(exc)})


def _check_auth(request: Request) -> None:
    token = request.headers.get("Authorization", "")
    if token != f"Bearer {API_KEY}":
        logger.warning("Invalid API key", token=token)
        raise AuthenticationError("Invalid API key")


def _check_rate_limit(request: Request) -> None:
    key = request.client.host
    now = time.time()
    window = RATE_LIMIT.setdefault(key, [])
    window[:] = [t for t in window if now - t < WINDOW_SECONDS]
    if len(window) >= MAX_REQUESTS:
        logger.warning("Rate limit exceeded", client=key)
        raise RateLimitError("Rate limit exceeded")
    window.append(now)


@app.get("/sse")
async def sse_endpoint(request: Request, client_id: str, close: bool = False) -> Any:
    _check_auth(request)
    _check_rate_limit(request)
    await log_info("SSE connection", client_id=client_id, close=close)
    return await transport.connect(client_id, close=close)


class RPCRequest(BaseModel):  # We'll need to import BaseModel at top
    id: str = Field(..., min_length=1)
    method: str = Field(..., min_length=1)
    params: Dict[str, Any] = Field(default_factory=dict)
    client_id: str | None = None


@app.post("/rpc")
async def rpc_endpoint(req: RPCRequest, request: Request) -> JSONResponse:
    _check_auth(request)
    _check_rate_limit(request)
    await log_info("RPC call", method=req.method)
    if req.method == "tools/list":
        result = {"tools": list(TOOLS.keys())}
    else:
        tool = TOOLS.get(req.method)
        if not tool:
            raise HTTPException(status_code=404, detail="Method not found")
        try:
            result = await tool(req.params)
        except ToolExecutionError as exc:
            logger.error("Tool execution failed", method=req.method, error=str(exc))
            raise HTTPException(status_code=400, detail=str(exc)) from exc
    response = {"jsonrpc": "2.0", "id": req.id, "result": result}
    if req.client_id:
        await transport.send(req.client_id, response)
    return JSONResponse(response)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.mcp.mcp_server:app", host="0.0.0.0", port=8051)
