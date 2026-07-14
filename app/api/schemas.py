from pydantic import BaseModel, Field

class GenerateRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=300,
        description="Text to convert into talking avatar video",
    )


class GenerateResponse(BaseModel):
    task_id: str


class StatusResponse(BaseModel):
    task_id: str
    status: str

class ResultResponse(BaseModel):
    task_id: str
    status: str
    download_url: str | None = None