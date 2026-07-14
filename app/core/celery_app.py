from celery import Celery
import os

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0",
)

celery_app = Celery(
    "avatar_service",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

celery_app.conf.update(
    imports=("app.workers.tasks",),
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)