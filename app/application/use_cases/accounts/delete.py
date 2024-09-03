from app.application.dtos.accounts.delete_request import DeleteAccountRequest
from app.application.interfaces.interactor import Interactor
from app.application.interfaces.transaction_manager import ITransactionContextManager
from app.domain.accounts.exceptions import AccountNotFoundError
from app.domain.accounts.repository import IAccountRepository


class DeleteAccountUseCase(Interactor[DeleteAccountRequest, None]):
    def __init__(
            self,
            repository: IAccountRepository,
            transaction_manager: ITransactionContextManager
    ) -> None:
        self.__repository = repository
        self.__transaction_manager = transaction_manager

    async def __call__(self, request: DeleteAccountRequest) -> None:
        await self.__repository.delete(id=request.uid)
        await self.__transaction_manager.commit()
