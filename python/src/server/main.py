from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.utils import ExternalServiceError, fetch_with_retry


class ProcessRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=100)


app = FastAPI()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/process")
async def process(req: ProcessRequest) -> dict[str, str]:
    try:
        data = await fetch_with_retry("get")
    except ExternalServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return {"echo": req.text, "data": data.get("url", "")}


socket_app = app
