from typing import Protocol

from app.domain.accounts.entity import Account


class IAccountRepository(Protocol):
    async def create(self, entity: Account) -> None: ...

    async def find_all(self, limit: int = 10, offset: int = 0, **parameters) -> list[Account]: ...

    async def filter_by(self, **parameters) -> list[Account]: ...

    async def update(self, entity: Account) -> None: ...

    async def delete(self, **parameters) -> None: ...
