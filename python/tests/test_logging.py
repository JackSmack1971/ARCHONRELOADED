import importlib
import sys

import pytest


def _reload_logging(monkeypatch: pytest.MonkeyPatch, token: str):
    """Reload logging module with a specific token."""
    monkeypatch.setenv("LOGFIRE_TOKEN", token)
    sys.modules.pop("src.common.logging", None)
    return importlib.import_module("src.common.logging")


def test_logger_initializes_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _reload_logging(monkeypatch, "abc123")
    assert module.logger.DEFAULT_LOGFIRE_INSTANCE.config.token == "abc123"


def test_logger_initializes_without_token(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _reload_logging(monkeypatch, "")
    assert module.logger.DEFAULT_LOGFIRE_INSTANCE.config.token is None


@pytest.mark.asyncio
async def test_log_functions(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _reload_logging(monkeypatch, "")
    await module.log_info("test", value=1)
    await module.log_error("oops", code=2)
