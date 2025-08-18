"""Tool registry for MCP server."""

from __future__ import annotations

from .project_tools import TOOLS as project_tools
from .document_tools import TOOLS as document_tools
from .task_tools import TOOLS as task_tools

TOOLS = {**project_tools, **document_tools, **task_tools}

__all__ = ["TOOLS"]
