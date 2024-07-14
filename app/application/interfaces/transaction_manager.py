from typing import Protocol


class ITransactionContextManager(Protocol):
    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...
