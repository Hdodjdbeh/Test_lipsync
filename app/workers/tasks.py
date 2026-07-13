import time

from app.core.celery_app import celery_app


@celery_app.task
def generate_avatar(text: str):
    print(f"Start generating video for: {text}")

    time.sleep(5)

    print("Generation completed!")

    return {
        "status": "completed",
    }