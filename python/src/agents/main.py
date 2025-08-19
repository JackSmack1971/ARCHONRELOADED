from fastapi import HTTPException
from pydantic import BaseModel, Field

from src.common.service import create_service
from src.common.logging import log_error, log_info
from src.utils import ExternalServiceError


class TaskRequest(BaseModel):
    task: str = Field(..., min_length=1, max_length=100)


app = create_service()


@app.post("/run")
async def run(req: TaskRequest) -> dict[str, str]:
    try:
        if req.task != "compute":
            await log_error("Unsupported task", task=req.task)
            raise ExternalServiceError("Unsupported task")
        await log_info("Task completed", task=req.task)
    except ExternalServiceError as exc:
        await log_error("External service error", error=str(exc))
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"status": "completed"}
