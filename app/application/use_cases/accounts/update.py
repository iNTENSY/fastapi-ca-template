from sqlalchemy.exc import IntegrityError

from app.application.dtos.accounts.base_responses import AccountResponse
from app.application.dtos.accounts.update_request import UpdateRequest
from app.application.interfaces.interactor import Interactor
from app.application.interfaces.transaction_manager import ITransactionContextManager
from app.domain.accounts.entity import Account
from app.domain.accounts.exceptions import AccountNotFoundError
from app.domain.accounts.repository import IAccountRepository
from app.domain.core import exceptions


class UpdateAccountUseCase(Interactor[UpdateRequest, AccountResponse]):
    def __init__(
            self,
            repository: IAccountRepository,
            transaction_manager: ITransactionContextManager
    ) -> None:
        self.__repository = repository
        self.__transaction = transaction_manager

    async def __call__(self, request: UpdateRequest) -> AccountResponse:
        try:
            entity = await self.__update(request)
        except IntegrityError:
            await self.__transaction.rollback()
            raise exceptions.IntegrityError

        await self.__transaction.commit()
        return AccountResponse.create(entity)

    async def __update(self, request: UpdateRequest) -> Account:
        entity = await self.__repository.filter_by(id=request.uid)
        if not entity:
            raise AccountNotFoundError
        entity = entity[0].update(**vars(request))
        await self.__repository.update(entity)
        return entity
