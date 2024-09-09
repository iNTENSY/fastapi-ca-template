from typing import Any

from redis import asyncio as aioredis
from app.application.interfaces.cache import ICache
from app.infrastructure.cache.schema import RedisSchema


class RedisAdapter(ICache):
    def __init__(self, redis: aioredis.Redis):
        self.__redis = redis

    async def get(self, key: Any) -> Any:
        cached_value = await self.__redis.get(key)
        return cached_value

    async def set(self, *collections: RedisSchema) -> None:
        for item in collections:
            await self.__redis.set(item.name, item.value, ex=item.ex)

    async def delete(self, *keys: str) -> None:
        await self.__redis.delete(*keys)

    @property
    def engine(self) -> aioredis.Redis:
        return self.__redis

    async def close(self) -> None:
        await self.__redis.close()
