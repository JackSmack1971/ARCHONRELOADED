import asyncio
import asyncio
import socketio
import uvicorn

from server.main import app
from server.socket import broadcast_upload_progress, broadcast_search_completed


def test_realtime_events():
    async def runner() -> None:
        config = uvicorn.Config(app, host="127.0.0.1", port=9000, log_level="warning")
        server = uvicorn.Server(config)
        server_task = asyncio.create_task(server.serve())
        await asyncio.sleep(0.3)

        client1 = socketio.AsyncClient()
        client2 = socketio.AsyncClient()

        await client1.connect("http://127.0.0.1:9000?user_id=u1")
        await client1.emit("project_join", {"project_id": "p1"})

        join_future: asyncio.Future = asyncio.Future()

        @client1.on("user:join")
        def _on_join(data: dict) -> None:
            if not join_future.done():
                join_future.set_result(data)

        await client2.connect("http://127.0.0.1:9000?user_id=u2")
        await client2.emit("project_join", {"project_id": "p1"})

        join_data = await asyncio.wait_for(join_future, 1)
        assert join_data["user_id"] == "u2"

        progress_future: asyncio.Future = asyncio.Future()

        @client1.on("document:upload_progress")
        def _on_progress(data: dict) -> None:
            if not progress_future.done():
                progress_future.set_result(data)

        await broadcast_upload_progress("p1", {"doc_id": "d1", "status": "processing"})
        progress = await asyncio.wait_for(progress_future, 1)
        assert progress["status"] == "processing"

        search_future: asyncio.Future = asyncio.Future()

        @client1.on("search:completed")
        def _on_search(data: dict) -> None:
            if not search_future.done():
                search_future.set_result(data)

        await broadcast_search_completed("p1", {"query": "x", "results": []})
        search = await asyncio.wait_for(search_future, 1)
        assert search["query"] == "x"

        leave_future: asyncio.Future = asyncio.Future()

        @client1.on("user:leave")
        def _on_leave(data: dict) -> None:
            if not leave_future.done():
                leave_future.set_result(data)

        await client2.disconnect()
        leave = await asyncio.wait_for(leave_future, 1)
        assert leave["user_id"] == "u2"

        await client1.disconnect()
        server.should_exit = True
        await server_task

    asyncio.run(runner())
