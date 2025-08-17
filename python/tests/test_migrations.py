from pathlib import Path
from typing import List

import pytest

from src.server.database import MigrationError, run_sql


@pytest.mark.asyncio
async def test_run_sql(tmp_path) -> None:
    sql_file = tmp_path / "test.sql"
    sql_file.write_text("SELECT 1; SELECT 2;")
    executed: List[str] = []

    async def exec_stmt(stmt: str) -> None:
        executed.append(stmt)

    await run_sql(str(sql_file), exec_stmt)
    assert executed == ["SELECT 1", "SELECT 2"]


@pytest.mark.asyncio
async def test_run_sql_missing(tmp_path) -> None:
    with pytest.raises(MigrationError):
        await run_sql(str(tmp_path / "missing.sql"), lambda _: None)
