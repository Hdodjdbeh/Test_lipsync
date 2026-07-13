from app.db.database import SessionLocal
from app.db.models import Task, TaskStatus


def create_task(task_id: str, text_hash: str) -> None:
    with SessionLocal() as session:
        task = Task(
            id=task_id,
            text_hash=text_hash,
            status=TaskStatus.PENDING,
        )

        session.add(task)
        session.commit()


def get_task(task_id: str) -> Task | None:
    with SessionLocal() as session:
        return session.get(Task, task_id)


def update_status(task_id: str, status: TaskStatus):
    with SessionLocal() as session:
        task = session.get(Task, task_id)

        if task:
            task.status = status
            session.commit()