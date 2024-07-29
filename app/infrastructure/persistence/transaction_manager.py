from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces.transaction_manager import ITransactionContextManager


class TransactionContextManagerImp(ITransactionContextManager):
    __slots__ = ("connection",)

    def __init__(self, connection: AsyncSession) -> None:
        self.__connection = connection

    async def commit(self) -> None:
        await self.__connection.commit()

    async def rollback(self) -> None:
        await self.__connection.rollback()
