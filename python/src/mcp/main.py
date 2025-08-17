from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.utils import ExternalServiceError


class CommandRequest(BaseModel):
    command: str = Field(..., min_length=1, max_length=50)


app = FastAPI()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/execute")
async def execute(req: CommandRequest) -> dict[str, str]:
    try:
        if req.command != "ping":
            raise ExternalServiceError("Unknown command")
    except ExternalServiceError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"result": "pong"}
