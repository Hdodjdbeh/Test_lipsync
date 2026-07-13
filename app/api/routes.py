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
from app.db.crud import create_task
from app.utils.hashing import text_hash
from fastapi import HTTPException

from app.db.crud import get_task
router = APIRouter(
    prefix="/api",
    tags=["Avatar"],
)


@router.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest):

    task = generate_avatar.delay(request.text)

    create_task(
        task.id,
        text_hash(request.text),
    )

    return GenerateResponse(
        task_id=task.id,
    )
@router.get("/status/{task_id}", response_model=StatusResponse)
def status(task_id: str):

    task = get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return StatusResponse(
        task_id=task.id,
        status=task.status,
    )