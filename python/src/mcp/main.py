from fastapi import HTTPException
from pydantic import BaseModel, Field

from src.common.service import create_service
from src.utils import ExternalServiceError


class CommandRequest(BaseModel):
    command: str = Field(..., min_length=1, max_length=50)


app = create_service()


@app.post("/execute")
async def execute(req: CommandRequest) -> dict[str, str]:
    try:
        if req.command != "ping":
            raise ExternalServiceError("Unknown command")
    except ExternalServiceError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"result": "pong"}
