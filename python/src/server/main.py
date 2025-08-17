from pydantic import BaseModel, Field

from src.common.service import create_service
from src.utils import fetch_with_retry


class ProcessRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=100)


app = create_service()


@app.post("/process")
async def process(req: ProcessRequest) -> dict[str, str]:
    data = await fetch_with_retry("get")
    return {"echo": req.text, "data": data.get("url", "")}


socket_app = app
