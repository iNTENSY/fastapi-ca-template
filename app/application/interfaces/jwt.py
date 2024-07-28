import uuid
from typing import Protocol, Any

from app.domain.core.value_objects import EmailVO, UuidVO


class IJwtProcessor(Protocol):
    def generate_token(self, uid: uuid.UUID, email: str) -> str:
        raise NotImplementedError

    def parse(self, token: str) -> tuple[UuidVO, EmailVO]:
        raise NotImplementedError

    def refresh_token(self, token: str) -> str:
        raise NotImplementedError
