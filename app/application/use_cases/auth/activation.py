from app.application.dtos.authentication.activation_request import ActivationRequest
from app.application.dtos.authentication.base_responses import ActivationResponse
from app.application.interfaces.interactor import Interactor
from app.application.interfaces.redis import ICache
from app.application.interfaces.transaction_manager import ITransactionContextManager
from app.domain.accounts.exceptions import ActivationError, AccountNotFoundError
from app.domain.accounts.repository import IAccountRepository


class ActivationUseCase(Interactor[ActivationRequest, ActivationResponse]):
    def __init__(
            self,
            cache: ICache,
            repository: IAccountRepository,
            transaction_manager: ITransactionContextManager
    ) -> None:
        self.__cache = cache
        self.__repository = repository
        self.__transaction = transaction_manager

    async def __call__(self, request: ActivationRequest) -> ActivationResponse:
        expected_code = await self.__cache.get(f"phone-{request.email}")
        if not expected_code:
            raise ActivationError("Запроса на активацию аккаунта не поступало, либо время истекло.")
        if int(expected_code) != request.code:
            raise ActivationError("Неверный код активации")

        try:
            entity = (await self.__repository.filter_by(email=request.email))[0]
        except Exception as e:
            raise AccountNotFoundError

        if entity.is_verified:
            raise ActivationError("Аккаунт уже активирован")

        await self.__cache.delete(f"phone-{request.email}")
        entity.verified = True
        await self.__repository.update(entity)
        await self.__transaction.commit()
        return ActivationResponse.create("Аккаунт успешно активирован")
