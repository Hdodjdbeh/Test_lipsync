import time

from app.core.celery_app import celery_app
from app.db.crud import update_status
from app.db.models import TaskStatus

@celery_app.task(bind=True)
def generate_avatar(self, text: str):

    update_status(
        self.request.id,
        TaskStatus.PROCESSING,
    )

    print(f"Start generating video for: {text}")

    time.sleep(5)

    print("Generation completed!")

    update_status(
        self.request.id,
        TaskStatus.COMPLETED,
    )

    return {
        "status": "completed",
    }