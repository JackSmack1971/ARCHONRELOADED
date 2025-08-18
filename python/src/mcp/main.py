"""MCP server entry point."""

from __future__ import annotations

from .mcp_server import app

__all__ = ["app"]

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.mcp.mcp_server:app", host="0.0.0.0", port=8051)
