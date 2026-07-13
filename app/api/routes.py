from uuid import uuid4
from app.workers.tasks import generate_avatar
from fastapi import APIRouter
from celery.result import AsyncResult
from app.core.celery_app import celery_app
from app.api.schemas import (
    GenerateRequest,
    GenerateResponse,
    StatusResponse,
)

router = APIRouter(
    prefix="/api",
    tags=["Avatar"],
)


@router.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest):

    task = generate_avatar.delay(request.text)

    return GenerateResponse(
        task_id=task.id,
    )

@router.get("/status/{task_id}", response_model=StatusResponse)
def status(task_id: str):

    task = AsyncResult(task_id, app=celery_app)

    return StatusResponse(
        task_id=task.id,
        status=task.status,
    )