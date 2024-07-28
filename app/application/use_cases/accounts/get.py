from app.application.dtos.accounts.base_responses import AccountResponse
from app.application.dtos.accounts.get_request import GetAccountRequest
from app.application.interfaces.interactor import Interactor
from app.domain.accounts.exceptions import AccountNotFoundError
from app.domain.accounts.repository import IAccountRepository


class GetAccountUseCase(Interactor[GetAccountRequest, AccountResponse]):
    def __init__(self, repository: IAccountRepository) -> None:
        self.__repository = repository

    async def __call__(self, request: GetAccountRequest) -> AccountResponse:
        entity = await self.__repository.filter_by(id=request.uid)
        if not entity:
            raise AccountNotFoundError
        return AccountResponse.create(entity[0])
