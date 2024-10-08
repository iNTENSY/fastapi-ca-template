from typing import Protocol, Any

from app.infrastructure.services.internal.cache.schema import RedisSchema


class ICache(Protocol):
    async def get(self, key: Any) -> bytes | str:
        raise NotImplementedError

    async def set(self, *collections: RedisSchema) -> None:
        raise NotImplementedError

    async def delete(self, *keys: str) -> None:
        raise NotImplementedError

    async def close(self) -> None:
        raise NotImplementedError

    @property
    def engine(self):
        raise NotImplementedError
