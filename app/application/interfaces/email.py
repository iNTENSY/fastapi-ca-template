from email.message import EmailMessage
from typing import Protocol


class IEmailService(Protocol):
    def send_email(self, to: str, subject: str, body: str, message: EmailMessage = None):
        raise NotImplementedError
