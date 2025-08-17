"""MCP package providing server and tools."""

from __future__ import annotations


class ToolExecutionError(Exception):
    """Raised when a tool fails to execute."""


__all__ = ["ToolExecutionError"]
