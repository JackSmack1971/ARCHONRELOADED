"""Central logging utilities using Logfire.

Reads ``LOGFIRE_TOKEN`` from the environment and configures the
Logfire SDK. Exported helper functions are ``async`` so they can be
safely awaited inside request handlers.
"""

from __future__ import annotations

import os
from typing import Any

import logfire


# Configure Logfire using token from environment. ``send_to_logfire`` is
# enabled only when a token is present to avoid failing in local
# development environments.
logfire.configure(token=os.getenv("LOGFIRE_TOKEN"), send_to_logfire="if-token-present")

# Re-export the configured logger for modules that prefer direct access.
logger = logfire


async def log_info(message: str, **data: Any) -> None:
    """Log an informational message."""
    logger.info(message, **data)


async def log_warning(message: str, **data: Any) -> None:
    """Log a warning message."""
    logger.warning(message, **data)


async def log_error(message: str, **data: Any) -> None:
    """Log an error message."""
    logger.error(message, **data)


async def log_debug(message: str, **data: Any) -> None:
    """Log a debug message."""
    logger.debug(message, **data)


__all__ = ["logger", "log_info", "log_warning", "log_error", "log_debug"]
