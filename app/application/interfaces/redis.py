from typing import Protocol, Any


class IRedis(Protocol):
    async def get(self, key: Any) -> bytes: ...

    async def set(self, *collections: dict) -> None: ...

    async def delete(self, *keys: str) -> None: ...

    async def close(self) -> None: ...

    @property
    def redis(self):
        raise NotImplementedError
