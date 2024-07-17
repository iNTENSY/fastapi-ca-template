from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.accounts.entity import Account
from app.domain.accounts.repository import IAccountRepository
from app.infrastructure.persistence.mappers.account import AccountMapper
from app.infrastructure.persistence.models import AccountModel


class AccountRepositoryImp(IAccountRepository):
    def __init__(self, connection: AsyncSession):
        self.__connection = connection

    async def create(self, entity: Account) -> None:
        statement = insert(AccountModel).values(**AccountMapper.generate_to_dict(entity))
        await self.__connection.execute(statement)

    async def filter_by(self, **parameters) -> list[Account]:
        statement = select(AccountModel).filter_by(**parameters)
        result = (await self.__connection.execute(statement)).mappings().all()
        return [AccountMapper.generate_to_entity(vars(item)) for item in result]

    async def find_all(self, limit: int = 10, offset: int = 0, **parameters) -> list[Account]:
        statement = select(AccountModel).limit(limit).offset(offset)
        if parameters:
            statement = statement.filter_by(**parameters)
        result = (await self.__connection.execute(statement)).scalars().all()
        return [AccountMapper.generate_to_entity(vars(contact)) for contact in result]

    async def update(self, entity: Account) -> None:
        statement = (
            update(AccountModel)
            .where(AccountModel.id == entity.id.value)
            .values(**AccountMapper.generate_to_dict(entity))
        )
        await self.__connection.execute(statement)
