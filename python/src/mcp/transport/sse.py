"""Simple SSE transport implementation."""

from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator
from typing import Dict

from fastapi.responses import StreamingResponse


class SSETransport:
    """Manage Server-Sent Events connections."""

    def __init__(self) -> None:
        self._clients: Dict[str, asyncio.Queue[str]] = {}

    async def connect(self, client_id: str, close: bool = False) -> StreamingResponse:
        queue: asyncio.Queue[str] = asyncio.Queue()
        self._clients[client_id] = queue

        async def event_generator() -> AsyncIterator[bytes]:
            try:
                yield b"data: connected\n\n"
                if close:
                    return
                while True:
                    data = await queue.get()
                    yield f"data: {data}\n\n".encode()
            finally:
                self._clients.pop(client_id, None)

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    async def send(self, client_id: str, message: dict) -> None:
        if client_id in self._clients:
            await self._clients[client_id].put(json.dumps(message))
