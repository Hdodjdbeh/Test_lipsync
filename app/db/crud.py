import logging

logger = logging.getLogger(__name__)
from app.db.database import SessionLocal
from app.db.models import Task, TaskStatus
from sqlalchemy import select

def create_task(task_id: str, text_hash: str) -> None:
    with SessionLocal() as session:
        task = Task(
            id=task_id,
            text_hash=text_hash,
            status=TaskStatus.PENDING,
        )

        session.add(task)
        session.commit()
        logger.info("Created task %s", task_id)


def get_task(task_id: str) -> Task | None:
    with SessionLocal() as session:
        return session.get(Task, task_id)


def update_status(task_id: str, status: TaskStatus):
    with SessionLocal() as session:
        task = session.get(Task, task_id)

        if task:
            task.status = status
            session.commit()
            logger.info(
                "Task %s status changed to %s",
                task_id,
                status.value,
            )

def finish_task(task_id: str, video_path: str):
    with SessionLocal() as session:
        task = session.get(Task, task_id)

        if task:
            task.status = TaskStatus.COMPLETED
            task.video_path = video_path
            session.commit()
            logger.info(
                "Task %s completed. Video: %s",
                task_id,
                video_path,
            )


def fail_task(task_id: str, error: str):
    with SessionLocal() as session:
        task = session.get(Task, task_id)

        if task:
            task.status = TaskStatus.FAILED
            task.error = error
            session.commit()
            logger.error(
                "Task %s failed: %s",
                task_id,
                error,
            )

def get_task_by_hash(text_hash: str) -> Task | None:
    with SessionLocal() as session:
        statement = (
            select(Task)
            .where(
                Task.text_hash == text_hash,
                Task.status == TaskStatus.COMPLETED,
            )
        )

        return session.scalar(statement)