import random

from app.infrastructure.services.tasks.celery import app


@app.task
def send_verification_code(*args, **kwargs) -> None:
    print(args, kwargs)
    code = random.randint(100000, 999999)
