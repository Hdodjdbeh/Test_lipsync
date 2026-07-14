from app.workers.tasks import generate_avatar
from app.api.schemas import (
    GenerateRequest,
    GenerateResponse,
    StatusResponse,
)
from app.utils.hashing import text_hash
from app.db.crud import (
    create_task,
    get_task,
    get_task_by_hash,
)
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.db.crud import get_task
from app.db.models import TaskStatus
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["Avatar"],
)


@router.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest):
    logger.info(
        "Generate request (%d chars)",
        len(request.text),
    )
    normalized_text = " ".join(request.text.split())
    hash_value = text_hash(normalized_text)

    cached_task = get_task_by_hash(hash_value)

    if (
            cached_task is not None
            and cached_task.status != TaskStatus.FAILED
    ):
        return GenerateResponse(
            task_id=cached_task.id,
        )

    task = generate_avatar.delay(request.text)

    create_task(
        task.id,
        hash_value,
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

@router.get("/result/{task_id}")
def get_result(task_id: str):

    task = get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    if task.status == TaskStatus.PENDING:
        raise HTTPException(
            status_code=409,
            detail="Task is waiting",
        )

    if task.status == TaskStatus.PROCESSING:
        raise HTTPException(
            status_code=409,
            detail="Task is processing",
        )

    if task.status == TaskStatus.FAILED:
        raise HTTPException(
            status_code=500,
            detail=task.error,
        )

    return FileResponse(
        task.video_path,
        media_type="video/mp4",
        filename=Path(task.video_path).name,
    )