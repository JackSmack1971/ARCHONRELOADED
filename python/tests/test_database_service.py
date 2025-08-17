from __future__ import annotations

from types import SimpleNamespace
from typing import Any, Dict, List
from uuid import uuid4

import pytest

from src.server.models.document import Document
from src.server.models.project import Project
from src.server.models.query import Query
from src.server.models.source import Source, SourceType
from src.server.services import DatabaseError, DatabaseService


class FakeExecute:
    def __init__(self, data: Any) -> None:
        self._data = data

    async def execute(self) -> Any:
        return SimpleNamespace(data=self._data)


class FakeSelect:
    def __init__(self, table: "FakeTable", updates: Dict[str, Any] | None = None) -> None:
        self.table = table
        self.filters: Dict[str, Any] = {}
        self.single_mode = False
        self.updates = updates

    def eq(self, field: str, value: str) -> "FakeSelect":
        self.filters[field] = value
        return self

    def single(self) -> "FakeSelect":
        self.single_mode = True
        return self

    def select(self, *_: str) -> "FakeSelect":
        return self

    def delete(self) -> "FakeSelect":
        self._delete = True
        return self

    def update(self, updates: Dict[str, Any]) -> "FakeSelect":
        self.updates = updates
        return self

    async def execute(self) -> Any:
        rows = [r for r in self.table.rows if all(str(r[k]) == v for k, v in self.filters.items())]
        if hasattr(self, "_delete"):
            self.table.rows = [r for r in self.table.rows if r not in rows]
            return SimpleNamespace(data=None)
        if self.updates and rows:
            rows[0].update(self.updates)
        if self.single_mode:
            return SimpleNamespace(data=rows[0] if rows else None)
        return SimpleNamespace(data=rows)


class FakeTable:
    def __init__(self, rows: List[Dict[str, Any]]) -> None:
        self.rows = rows

    def insert(self, data: Dict[str, Any]) -> FakeExecute:
        self.rows.append(data)
        return FakeExecute([data])

    def select(self, *_: str) -> FakeSelect:
        return FakeSelect(self)

    def update(self, data: Dict[str, Any]) -> FakeSelect:
        return FakeSelect(self, updates=data)

    def delete(self) -> FakeSelect:
        return FakeSelect(self).delete()


class FakePostgrest:
    class Tx:
        async def __aenter__(self) -> "FakePostgrest.Tx":
            return self

        async def __aexit__(self, exc_type, exc, tb) -> None:  # noqa: D401
            return None

        async def rollback(self) -> None:  # noqa: D401
            return None

    def transaction(self) -> "FakePostgrest.Tx":
        return FakePostgrest.Tx()


class FakeSupabase:
    def __init__(self) -> None:
        self.tables: Dict[str, List[Dict[str, Any]]] = {
            "projects": [],
            "sources": [],
            "documents": [],
            "embeddings": [],
        }
        self.postgrest = FakePostgrest()

    def table(self, name: str) -> FakeTable:
        return FakeTable(self.tables[name])

    def rpc(self, name: str, params: Dict[str, Any]) -> FakeExecute:
        if name == "match_documents":
            data = self.tables["documents"][: params["match_count"]]
        elif name == "match_embeddings":
            data = self.tables["embeddings"][: params["match_count"]]
        else:
            data = []
        return FakeExecute(data)


class FakeClientProvider:
    def __init__(self) -> None:
        self.client = FakeSupabase()

    async def get_client(self) -> FakeSupabase:
        return self.client


@pytest.mark.asyncio
async def test_database_service_flow() -> None:
    provider = FakeClientProvider()
    service = DatabaseService(provider)

    project = await service.create_project(Project(id=uuid4(), name="p"))
    assert (await service.get_project(project.id)).id == project.id
    assert len(await service.list_projects()) == 1
    await service.update_project(project.id, {"name": "p2"})

    source = await service.create_source(
        Source(id=uuid4(), project_id=project.id, type=SourceType.WEB, url="https://x.com")
    )
    assert len(await service.list_sources(project.id)) == 1

    doc = await service.create_document(
        Document(id=uuid4(), source_id=source.id, content="hi")
    )
    assert len(await service.vector_search([0.1, 0.2], Query(query_text="x"))) == 1

    assert await service.store_embedding(doc.id, [0.1, 0.2]) is True
    assert len(await service.similarity_query([0.1, 0.2], 1)) == 1

    assert await service.delete_document(doc.id) is True
    assert await service.delete_source(source.id) is True
    assert await service.delete_project(project.id) is True

    async def failing(_: Any) -> None:
        raise ValueError("boom")

    with pytest.raises(DatabaseError):
        await service.transaction(failing)
