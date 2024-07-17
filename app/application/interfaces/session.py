import uuid

from typing import Protocol

from app.infrastructure.cache.schema import RedisSchema


class ISessionProcessor(Protocol):
    async def generate_session(self, account_id: uuid.UUID) -> RedisSchema: ...

    async def validate(self, session: str): ...

    async def delete_session(self, session: str) -> None: ...
