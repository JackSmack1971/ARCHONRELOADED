"""Tool registry for MCP server."""

from __future__ import annotations

from .project_tools import TOOLS as project_tools
from .rag_tools import TOOLS as rag_tools
from .source_tools import TOOLS as source_tools

TOOLS = {**project_tools, **source_tools, **rag_tools}

__all__ = ["TOOLS"]
