import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from typing import Any

from app.infrastructure.background_tasks.celery import app


@app.task()
def send_verification_code(conf: dict[str, Any], to: str, message: str) -> None:
    with smtplib.SMTP(conf["host"], conf["port"]) as server:
        server.starttls()
        server.login(conf["login"], conf["password"])
        server.sendmail(
            from_addr=conf["login"],
            to_addrs=to,
            msg=message
        )
