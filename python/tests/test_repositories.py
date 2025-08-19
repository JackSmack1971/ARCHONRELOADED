import pytest
import httpx

from src.server.repositories import (
    BaseRepository,
    SupabaseRepository,
    SupabaseRepositoryError,
)


class FakeResponse:
    def __init__(self, data):
        self.data = data


class FakeBuilder:
    def __init__(self, data, raise_error=False):
        self.data = data
        self.raise_error = raise_error

    async def execute(self):
        if self.raise_error:
            raise httpx.HTTPError("boom")
        return FakeResponse(self.data)


class FakeTable:
    def __init__(self, response=None, raise_error=False):
        self.response = response or {}
        self.raise_error = raise_error

    def insert(self, data):
        return FakeBuilder(data, self.raise_error)

    def select(self, *_):
        return self

    def eq(self, *_):
        return self

    def single(self):
        return FakeBuilder(self.response, self.raise_error)

    def update(self, data):
        return FakeBuilder(data, self.raise_error)

    def delete(self):
        return FakeBuilder(self.response, self.raise_error)


class FakeClient:
    def __init__(self, response=None, raise_error=False):
        self.response = response or {}
        self.raise_error = raise_error

    def table(self, _name):
        return FakeTable(self.response, self.raise_error)


def test_base_repository_abstract():
    with pytest.raises(TypeError):
        BaseRepository()


@pytest.mark.asyncio
async def test_supabase_repository_crud_success():
    client = FakeClient({"id": 1, "name": "x"})
    repo: SupabaseRepository[dict[str, str]] = SupabaseRepository(client, "items")
    ok, created = await repo.create({"name": "x"})
    assert ok and created["name"] == "x"
    ok, fetched = await repo.read(1)
    assert ok and fetched["id"] == 1
    ok, updated = await repo.update(1, {"name": "y"})
    assert ok and updated["name"] == "y"
    ok, deleted = await repo.delete(1)
    assert ok and "id" in deleted


@pytest.mark.asyncio
async def test_supabase_repository_invalid_input():
    client = FakeClient()
    repo: SupabaseRepository[dict[str, str]] = SupabaseRepository(client, "items")
    with pytest.raises(SupabaseRepositoryError):
        await repo.create({})
    with pytest.raises(SupabaseRepositoryError):
        await repo.read("")


@pytest.mark.asyncio
async def test_supabase_repository_failure():
    client = FakeClient(raise_error=True)
    repo: SupabaseRepository[dict[str, str]] = SupabaseRepository(client, "items")
    ok, result = await repo.read(1)
    assert not ok and "error" in result
