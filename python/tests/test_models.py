from __future__ import annotations

import pytest
from pydantic import ValidationError
from uuid import UUID

from src.server.models import (
    Document,
    Project,
    ProjectStatus,
    Query,
    ResponseModel,
    ResponseStatus,
    Source,
    SourceStatus,
    SourceType,
)


def test_project_name_length_validation() -> None:
    with pytest.raises(ValidationError):
        Project(
            id=UUID("12345678-1234-5678-1234-567812345678"),
            name="x" * 101,
            description="desc",
        )


def test_source_url_validation() -> None:
    with pytest.raises(ValidationError):
        Source(
            id=UUID("12345678-1234-5678-1234-567812345678"),
            project_id=UUID("12345678-1234-5678-1234-567812345679"),
            type=SourceType.WEB,
            url="not-a-url",
            status=SourceStatus.PENDING,
        )


def test_document_uuid_validation() -> None:
    with pytest.raises(ValidationError):
        Document(
            id=UUID("12345678-1234-5678-1234-567812345670"),
            source_id=UUID("12345678-1234-5678-1234-567812345671"),
            content="text",
        )


def test_query_threshold_validation() -> None:
    with pytest.raises(ValidationError):
        Query(query_text="hello", threshold=1.5)


def test_response_model_error_required() -> None:
    with pytest.raises(ValidationError):
        ResponseModel(status=ResponseStatus.ERROR)


def test_response_model_success() -> None:
    result = ResponseModel(status=ResponseStatus.SUCCESS, data={"ok": True})
    assert result.data == {"ok": True}
