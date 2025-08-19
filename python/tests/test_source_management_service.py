import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "source_management_service",
    Path(__file__).parents[1] / "src/server/services/source_management_service.py",
)
if spec is None or spec.loader is None:
    raise ImportError("module spec not found")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
SourceManagementService = module.SourceManagementService
SourceManagementError = module.SourceManagementError


class GoodRepo:
    async def list_sources(self):
        return True, {"sources": [{"id": "1"}]}

    async def delete(self, source_id: str):
        return True, {"source": source_id}

    async def update(self, source_id: str, metadata: dict):
        return True, {"source": source_id, "metadata": metadata}


class FailingRepo:
    async def list_sources(self):
        return False, {"error": "db"}

    async def delete(self, source_id: str):
        return False, {"error": "missing"}

    async def update(self, source_id: str, metadata: dict):
        raise RuntimeError("boom")


@pytest.mark.asyncio
async def test_get_available_sources_success():
    service = SourceManagementService(GoodRepo())
    ok, data = await service.get_available_sources()
    assert ok is True
    assert data["total_count"] == 1


@pytest.mark.asyncio
async def test_get_available_sources_failure():
    service = SourceManagementService(FailingRepo())
    ok, data = await service.get_available_sources()
    assert ok is False
    assert data["error"] == "db"


@pytest.mark.asyncio
async def test_delete_source_validation():
    service = SourceManagementService(GoodRepo())
    ok, data = await service.delete_source("")
    assert ok is False
    assert "error" in data


@pytest.mark.asyncio
async def test_delete_source_failure():
    service = SourceManagementService(FailingRepo())
    ok, data = await service.delete_source("abc")
    assert ok is False
    assert data["error"] == "missing"


@pytest.mark.asyncio
async def test_update_source_metadata_success():
    service = SourceManagementService(GoodRepo())
    ok, data = await service.update_source_metadata("1", {"a": 1})
    assert ok is True
    assert data["metadata"]["a"] == 1


@pytest.mark.asyncio
async def test_update_source_metadata_invalid_input():
    service = SourceManagementService(GoodRepo())
    ok, data = await service.update_source_metadata("", {})
    assert ok is False
    assert "error" in data


@pytest.mark.asyncio
async def test_update_source_metadata_exception():
    service = SourceManagementService(FailingRepo())
    with pytest.raises(SourceManagementError):
        await service.update_source_metadata("1", {"a": 1})
