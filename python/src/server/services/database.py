from __future__ import annotations

from typing import Any, Awaitable, Callable, Dict, List, Optional, Sequence
from uuid import UUID

from supabase import AsyncClient

from ..models.document import Document
from ..models.project import Project
from ..models.query import Query
from ..models.source import Source
from .supabase_client import SupabaseClient


class DatabaseError(Exception):
    """Raised when database operations fail."""


class DatabaseService:
    """Service layer providing CRUD and vector operations."""

    def __init__(self, client: SupabaseClient) -> None:
        self._client = client

    async def _table(self, name: str):
        sb = await self._client.get_client()
        return sb.table(name)

    async def create_project(self, project: Project) -> Project:
        try:
            tbl = await self._table("projects")
            res = await tbl.insert(project.model_dump()).execute()
            return Project(**res.data[0])
        except Exception as exc:
            raise DatabaseError("create_project failed") from exc

    async def get_project(self, project_id: UUID) -> Optional[Project]:
        try:
            tbl = await self._table("projects")
            res = await tbl.select("*").eq("id", str(project_id)).single().execute()
            return Project(**res.data)
        except Exception:
            return None

    async def update_project(self, project_id: UUID, data: Dict[str, Any]) -> Optional[Project]:
        try:
            tbl = await self._table("projects")
            res = (
                await tbl.update(data).eq("id", str(project_id)).select("*").single().execute()
            )
            return Project(**res.data)
        except Exception:
            return None

    async def delete_project(self, project_id: UUID) -> bool:
        try:
            tbl = await self._table("projects")
            await tbl.delete().eq("id", str(project_id)).execute()
            return True
        except Exception:
            return False

    async def list_projects(self) -> List[Project]:
        tbl = await self._table("projects")
        res = await tbl.select("*").execute()
        return [Project(**row) for row in res.data]

    async def create_source(self, source: Source) -> Source:
        try:
            tbl = await self._table("sources")
            res = await tbl.insert(source.model_dump()).execute()
            return Source(**res.data[0])
        except Exception as exc:
            raise DatabaseError("create_source failed") from exc

    async def get_source(self, source_id: UUID) -> Optional[Source]:
        try:
            tbl = await self._table("sources")
            res = await tbl.select("*").eq("id", str(source_id)).single().execute()
            return Source(**res.data)
        except Exception:
            return None

    async def update_source(self, source_id: UUID, data: Dict[str, Any]) -> Optional[Source]:
        try:
            tbl = await self._table("sources")
            res = (
                await tbl.update(data).eq("id", str(source_id)).select("*").single().execute()
            )
            return Source(**res.data)
        except Exception:
            return None

    async def delete_source(self, source_id: UUID) -> bool:
        try:
            tbl = await self._table("sources")
            await tbl.delete().eq("id", str(source_id)).execute()
            return True
        except Exception:
            return False

    async def list_sources(self, project_id: UUID) -> List[Source]:
        tbl = await self._table("sources")
        res = await tbl.select("*").eq("project_id", str(project_id)).execute()
        return [Source(**row) for row in res.data]

    async def create_document(self, doc: Document) -> Document:
        try:
            tbl = await self._table("documents")
            res = await tbl.insert(doc.model_dump()).execute()
            return Document(**res.data[0])
        except Exception as exc:
            raise DatabaseError("create_document failed") from exc

    async def get_document(self, doc_id: UUID) -> Optional[Document]:
        try:
            tbl = await self._table("documents")
            res = await tbl.select("*").eq("id", str(doc_id)).single().execute()
            return Document(**res.data)
        except Exception:
            return None

    async def update_document(self, doc_id: UUID, data: Dict[str, Any]) -> Optional[Document]:
        try:
            tbl = await self._table("documents")
            res = (
                await tbl.update(data).eq("id", str(doc_id)).select("*").single().execute()
            )
            return Document(**res.data)
        except Exception:
            return None

    async def delete_document(self, doc_id: UUID) -> bool:
        try:
            tbl = await self._table("documents")
            await tbl.delete().eq("id", str(doc_id)).execute()
            return True
        except Exception:
            return False

    async def vector_search(self, embedding: Sequence[float], query: Query) -> List[Document]:
        sb = await self._client.get_client()
        try:
            res = await sb.rpc(
                "match_documents",
                {
                    "query_embedding": list(embedding),
                    "match_count": query.match_count,
                    "filter": query.filters,
                    "threshold": query.threshold,
                },
            ).execute()
            return [Document(**row) for row in res.data]
        except Exception as exc:
            raise DatabaseError("vector_search failed") from exc

    async def store_embedding(self, doc_id: UUID, embedding: Sequence[float]) -> bool:
        try:
            tbl = await self._table("embeddings")
            await tbl.insert({"doc_id": str(doc_id), "embedding": list(embedding)}).execute()
            return True
        except Exception:
            return False

    async def similarity_query(self, embedding: Sequence[float], top_k: int) -> List[Dict[str, Any]]:
        sb = await self._client.get_client()
        res = await sb.rpc(
            "match_embeddings",
            {"query_embedding": list(embedding), "match_count": top_k},
        ).execute()
        return res.data

    async def transaction(self, func: Callable[[AsyncClient], Awaitable[Any]]) -> Any:
        sb = await self._client.get_client()
        async with sb.postgrest.transaction() as tx:
            try:
                return await func(tx)
            except Exception as exc:
                await tx.rollback()
                raise DatabaseError("transaction failed") from exc
