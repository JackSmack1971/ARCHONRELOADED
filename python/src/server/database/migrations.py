from __future__ import annotations

from pathlib import Path
from typing import Awaitable, Callable

from opentelemetry import trace


class MigrationError(Exception):
    """Raised when a migration fails."""


tracer = trace.get_tracer(__name__)


async def run_sql(path: str, executor: Callable[[str], Awaitable[None]]) -> None:
    """Execute SQL statements from a file using the provided executor.

    Args:
        path: Path to the SQL file.
        executor: Async callable executing a single SQL statement.
    """
    try:
        sql = Path(path).read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise MigrationError("migration file not found") from exc

    for statement in [s.strip() for s in sql.split(";") if s.strip()]:
        with tracer.start_as_current_span("sql.execute", {"db.statement": statement}) as span:
            try:
                await executor(statement)
            except Exception as exc:  # noqa: BLE001
                span.record_exception(exc)
                raise MigrationError(f"failed statement: {statement}") from exc
