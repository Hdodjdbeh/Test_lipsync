from app.core.celery_app import celery_app
from app.db.crud import (
    update_status,
    finish_task,
    fail_task,
)
from app.db.models import TaskStatus
from app.ml.pipeline import get_pipeline
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True)
def generate_avatar(self, text: str):
    pipeline = get_pipeline()

    try:
        logger.info(
            "Started avatar generation: %s",
            self.request.id,
        )
        update_status(
            self.request.id,
            TaskStatus.PROCESSING,
        )

        video_path = pipeline.generate(
            task_id=self.request.id,
            text=text,
        )

        finish_task(
            self.request.id,
            video_path.as_posix(),
        )
        logger.info(
            "Task %s completed",
            self.request.id,
        )
        return video_path.as_posix()


    except Exception as e:

        logger.exception(
            "Task %s failed",
            self.request.id,
        )
        fail_task(
            self.request.id,
            str(e),
        )
        raise