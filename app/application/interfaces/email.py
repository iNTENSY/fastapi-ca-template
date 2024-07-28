from typing import Protocol


class IEmailService(Protocol):
    def send_email(self, to: str, subject: str, body: str) -> None:
        raise NotImplementedError
