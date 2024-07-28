from app.application.dtos.accounts.base_responses import AccountsResponse
from app.application.dtos.accounts.get_request import GetAccountsRequest
from app.application.interfaces.interactor import Interactor
from app.domain.accounts.repository import IAccountRepository


class GetAccountsUseCase(Interactor[GetAccountsRequest, AccountsResponse]):
    def __init__(self, repository: IAccountRepository) -> None:
        self.__repository = repository

    async def __call__(self, request: GetAccountsRequest) -> AccountsResponse:
        entities = await self.__repository.find_all(limit=request.limit, offset=request.offset)
        return AccountsResponse.create(entities)
