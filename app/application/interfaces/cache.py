from typing import Protocol, Any

from app.infrastructure.cache.schema import RedisSchema


class ICache(Protocol):
    async def get(self, key: Any) -> bytes:
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
