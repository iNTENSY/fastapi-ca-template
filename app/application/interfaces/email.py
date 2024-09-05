from email.message import EmailMessage
from email.mime.text import MIMEText
from typing import Protocol


class IEmailService(Protocol):
    def send_email(self, message: EmailMessage | MIMEText) -> None:
        raise NotImplementedError

    def generate_simple_message(self, to: str, subject: str, body: str) -> MIMEText:
        raise NotImplementedError
