from app.application.dtos.accounts.base_responses import BaseAccountsResponse
from app.application.dtos.accounts.password_request import ResetPasswordRequest
from app.application.interfaces.interactor import Interactor
from app.application.interfaces.password_hasher import IPasswordHasher
from app.application.interfaces.cache import ICache
from app.application.interfaces.transaction_manager import ITransactionContextManager
from app.domain.accounts.entity import Account
from app.domain.accounts.exceptions import AccountNotFoundError, UserBadPermissionError, CacheError
from app.domain.accounts.repository import IAccountRepository


class ResetPasswordUseCase(Interactor[ResetPasswordRequest, BaseAccountsResponse]):
    def __init__(
            self,
            repository: IAccountRepository,
            pwd_hasher: IPasswordHasher,
            transaction_manager: ITransactionContextManager,
            cache: ICache
    ) -> None:
        self.__repository = repository
        self.__pwd_hasher = pwd_hasher
        self.__transaction = transaction_manager
        self.__cache = cache

    async def __call__(self, request: ResetPasswordRequest) -> BaseAccountsResponse:
        try:
            entity = await self.__get(request.email)
        except IndexError:
            raise AccountNotFoundError

        await self.__validate_code(request.code, request.email)
        await self.__update(entity, request.password)
        return BaseAccountsResponse.create("Пароль был успешно обновлен.")

    async def __get(self, email: str) -> Account:
        entity = await self.__repository.filter_by(email=email)
        return entity[0]

    async def __validate_code(self, code: str, email: str) -> None:
        key = f"reset-pwd-{email}"
        cached_code = await self.__cache.get(key)

        if not cached_code:
            raise CacheError("Запроса на смену пароля не поступало")
        if str(cached_code) != str(code):
            raise UserBadPermissionError

        await self.__cache.delete(key)

    async def __update(self, entity: Account, password: str) -> Account:
        hashed_password = self.__pwd_hasher.hash_password(password)
        entity.update(password=hashed_password)
        await self.__repository.update(entity)
        return entity
