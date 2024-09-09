import uuid

from typing import Protocol


class ISessionProcessor(Protocol):
    async def generate_session(self, account_id: uuid.UUID) -> str:
        raise NotImplementedError

    async def validate(self, session: str) -> tuple[str, str]:
        raise NotImplementedError

    async def delete_session(self, session: str) -> None:
        raise NotImplementedError
