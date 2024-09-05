from celery import Celery

app = Celery(
    "app",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["app.infrastructure.services.tasks.tasks"]
)

