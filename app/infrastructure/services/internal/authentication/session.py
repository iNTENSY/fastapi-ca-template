import random
import string
import uuid

from app.application.interfaces.cache import ICache
from app.application.interfaces.session import ISessionProcessor
from app.domain.accounts.exceptions import UserIsNotAuthorizedError
from app.infrastructure.cache.schema import RedisSchema
from app.infrastructure.settings.session import SessionSettings


class SessionProcessorImp(ISessionProcessor):
    def __init__(self, redis: ICache, settings: SessionSettings):
        self.__redis = redis
        self.__settings = settings

    async def generate_session(self, account_id: uuid.UUID) -> str:
        session_id = "".join(random.choices(string.ascii_letters, k=30))
        session = RedisSchema.create(key=session_id, value=str(account_id), ex=self.__settings.timedelta)
        await self.__redis.set(session)
        return session_id

    async def validate(self, session: str) -> tuple[str, str]:
        value = await self.__redis.get(key=session)
        if value is None:
            raise UserIsNotAuthorizedError
        return session, value # noqa: Value is auto-decoded

    async def delete_session(self, session: str) -> None:
        key, value = await self.validate(session)
        await self.__redis.delete(key)
