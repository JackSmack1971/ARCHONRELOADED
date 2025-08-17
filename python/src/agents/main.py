from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.utils import ExternalServiceError


class TaskRequest(BaseModel):
    task: str = Field(..., min_length=1, max_length=100)


app = FastAPI()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/run")
async def run(req: TaskRequest) -> dict[str, str]:
    try:
        if req.task != "compute":
            raise ExternalServiceError("Unsupported task")
    except ExternalServiceError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"status": "completed"}
