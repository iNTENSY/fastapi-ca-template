from app.application.dtos.authentication.activation_request import ActivationRequest
from app.application.dtos.authentication.base_responses import ActivationResponse
from app.application.interfaces.interactor import Interactor
from app.application.interfaces.cache import ICache
from app.application.interfaces.transaction_manager import ITransactionContextManager
from app.domain.accounts.entity import Account
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
        expected_code = await self.__cache.get(f"activation-{request.email}")
        await self.__verify_activation_code(expected_code, request.code)

        entity = await self.__get_entity(request.email)
        await self.__cache.delete(f"activation-{request.email}")

        await self.__update_entity(entity, is_verified=True)
        await self.__transaction.commit()
        return ActivationResponse.create("Аккаунт успешно активирован")

    async def __verify_activation_code(self, expected_code: str, request_code: str) -> None:
        if not expected_code:
            raise ActivationError("Запроса на активацию аккаунта не поступало, либо время истекло.")
        if str(expected_code) != request_code:
            raise ActivationError("Неверный код активации")

    async def __get_entity(self, email: str) -> Account:
        entity = await self.__repository.filter_by(email=email)
        if not entity:
            raise AccountNotFoundError

        entity = entity[0]

        if entity.is_verified.value:
            raise ActivationError("Аккаунт уже активирован")
        return entity

    async def __update_entity(self, entity: Account, **fields) -> Account:
        entity.update(**fields)
        await self.__repository.update(entity)
        return entity
