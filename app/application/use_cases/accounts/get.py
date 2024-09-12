import uuid

from app.application.dtos.accounts.base_responses import AccountResponse
from app.application.dtos.accounts.get_request import GetAccountRequest
from app.application.interfaces.interactor import Interactor
from app.domain.accounts.entity import Account
from app.domain.accounts.exceptions import AccountNotFoundError
from app.domain.accounts.repository import IAccountRepository


class GetAccountByUidUseCase(Interactor[GetAccountRequest, AccountResponse]):
    def __init__(self, repository: IAccountRepository) -> None:
        self.__repository = repository

    async def __call__(self, request: GetAccountRequest) -> AccountResponse:
        entity = await self.__get_entity(id=request.uid)
        return AccountResponse.create(entity)

    async def __get_entity(self, id: uuid.UUID) -> Account:
        entity = await self.__repository.filter_by(id=id)
        if not entity:
            raise AccountNotFoundError
        return entity[0]
