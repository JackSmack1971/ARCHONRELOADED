from __future__ import annotations

from typing import Any, Dict, Set
from urllib.parse import parse_qs

from loguru import logger
import socketio

from .config import settings


class SocketSessionError(Exception):
    """Raised when a connection lacks required identification."""


class ProjectRoomError(Exception):
    """Raised when room operations fail."""


class BroadcastError(Exception):
    """Raised when event broadcasting fails."""


sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=settings.cors_origins)
_user_sessions: Dict[str, Set[str]] = {}


@sio.event
async def connect(sid: str, environ: Dict[str, Any]) -> None:
    """Handle a new Socket.IO connection."""
    try:
        query = parse_qs(environ.get("QUERY_STRING", ""))
        user_id = query.get("user_id", [""])[0]
        if not user_id:
            raise SocketSessionError("user_id required")
        await sio.save_session(sid, {"user_id": user_id})
        _user_sessions.setdefault(user_id, set()).add(sid)
        logger.info("socket connected", sid=sid, user_id=user_id)
    except Exception as exc:  # noqa: BLE001
        logger.error("socket connect error", error=str(exc))
        raise


@sio.event
async def disconnect(sid: str) -> None:
    """Handle Socket.IO disconnects."""
    session = await sio.get_session(sid)
    user_id = session.get("user_id") if session else None
    if user_id and sid in _user_sessions.get(user_id, set()):
        _user_sessions[user_id].discard(sid)
        if not _user_sessions[user_id]:
            _user_sessions.pop(user_id)
    rooms = sio.rooms(sid)
    for room in rooms:
        if room.startswith("project:"):
            await sio.emit("user:leave", {"user_id": user_id}, room=room, skip_sid=sid)
    logger.info("socket disconnected", sid=sid)


@sio.event
async def project_join(sid: str, data: Dict[str, Any]) -> None:
    """Join a project room and notify peers."""
    try:
        project_id = str(data.get("project_id"))
        if not project_id:
            raise ProjectRoomError("project_id required")
        session = await sio.get_session(sid)
        await sio.enter_room(sid, f"project:{project_id}")
        await sio.emit(
            "user:join",
            {"user_id": session.get("user_id")},
            room=f"project:{project_id}",
            skip_sid=sid,
        )
    except Exception as exc:  # noqa: BLE001
        logger.error("project join error", error=str(exc))
        raise


@sio.event
async def project_leave(sid: str, data: Dict[str, Any]) -> None:
    """Leave a project room and notify peers."""
    project_id = str(data.get("project_id"))
    if not project_id:
        return
    await sio.leave_room(sid, f"project:{project_id}")
    session = await sio.get_session(sid)
    await sio.emit(
        "user:leave",
        {"user_id": session.get("user_id")},
        room=f"project:{project_id}",
        skip_sid=sid,
    )


async def broadcast_upload_progress(project_id: str, payload: Dict[str, Any]) -> None:
    """Broadcast document upload progress to a project room."""
    try:
        await sio.emit("document:upload_progress", payload, room=f"project:{project_id}")
    except Exception as exc:  # noqa: BLE001
        logger.error("upload progress broadcast failed", error=str(exc))
        raise BroadcastError from exc


async def broadcast_search_completed(project_id: str, payload: Dict[str, Any]) -> None:
    """Broadcast search completion results to a project room."""
    try:
        await sio.emit("search:completed", payload, room=f"project:{project_id}")
    except Exception as exc:  # noqa: BLE001
        logger.error("search broadcast failed", error=str(exc))
        raise BroadcastError from exc
