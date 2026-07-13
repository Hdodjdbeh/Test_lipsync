from uuid import uuid4

from fastapi import APIRouter

from app.api.schemas import (
    GenerateRequest,
    GenerateResponse,
    StatusResponse,
)

router = APIRouter()


@router.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest):
    return GenerateResponse(
        task_id=str(uuid4())
    )


@router.get("/status/{task_id}", response_model=StatusResponse)
def status(task_id: str):
    return StatusResponse(
        task_id=task_id,
        status="PENDING",
    )