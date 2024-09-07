from app.application.interfaces.interactor import Interactor
from app.application.interfaces.transaction_manager import ITransactionContextManager
from app.domain.accounts.entity import Account
from app.domain.accounts.repository import IAccountRepository


class UpdateAccountUseCase(Interactor[..., ...]):
    def __init__(
            self,
            repository: IAccountRepository,
            transaction_manager: ITransactionContextManager
    ) -> None:
        self.__repository = repository
        self.__transaction = transaction_manager

    async def __call__(self, request: ...) -> ...:
        try:
            ...
        except Exception as e:
            ...

    async def __update(self, request: ...) -> Account:
        entity = await self.__repository.filter_by(email=request.email)
        entity = await self.__repository.update(entity)
