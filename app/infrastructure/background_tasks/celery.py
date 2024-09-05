import os

from celery import Celery


_REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
_REDIS_PORT = os.environ.get("REDIS_PORT", 6379)

app = Celery(
    "app",
    broker=f"redis://{_REDIS_HOST}:{_REDIS_PORT}/0",
    backend=f"redis://{_REDIS_HOST}:{_REDIS_PORT}/0",
    include=[
        "app.infrastructure.services.external.email.tasks",
    ]
)
