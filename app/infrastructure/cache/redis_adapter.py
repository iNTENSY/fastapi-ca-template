from typing import Any

import aioredis

from app.application.interfaces.redis import IRedis
from app.infrastructure.cache.schema import RedisSchema


class RedisAdapter(IRedis):
    def __init__(self, redis: aioredis.client.Redis):
        self.__redis = redis

    async def get(self, key: Any) -> Any:
        cached_value = await self.__redis.get(key)
        return cached_value

    async def set(self, *collections: list[RedisSchema] | tuple[RedisSchema]) -> None:
        if not all(isinstance(collection, RedisSchema) for collection in collections):
            raise ValueError("All instance must be RedisSchema")

        for collection in collections:
            await self.__redis.set(**vars(collection))

    async def delete(self, *keys: str) -> None:
        await self.__redis.delete(*keys)

    @property
    def redis(self) -> aioredis.Redis:
        return self.__redis

    async def close(self) -> None:
        await self.__redis.close()
