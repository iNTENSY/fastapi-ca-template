import random
from typing import Any

from app.application.dtos.accounts.base_responses import BaseAccountsResponse
from app.application.dtos.accounts.password_request import ForgotPasswordRequest
from app.application.interfaces.email import IEmailService
from app.application.interfaces.interactor import Interactor
from app.application.interfaces.cache import ICache
from app.domain.accounts.entity import Account
from app.domain.accounts.exceptions import AccountNotFoundError, AccountBadPermissionError
from app.domain.accounts.repository import IAccountRepository
from app.infrastructure.services.internal.cache.schema import RedisSchema
from app.infrastructure.settings.core import Settings


class ForgotPasswordUseCase(Interactor[ForgotPasswordRequest, BaseAccountsResponse]):
    def __init__(
            self,
            repository: IAccountRepository,
            service: IEmailService,
            settings: Settings,
            cache: ICache
    ) -> None:
        self.__repository = repository
        self.__service = service
        self.__settings = settings
        self.__cache = cache

    async def __call__(self, request: ForgotPasswordRequest) -> BaseAccountsResponse:
        await self.__validate_entity_by_email(request.email)

        generated_code = self.__generate_special_code()
        email = request.email

        await self.__set_to_cache(email, generated_code)
        self.__send_email_message(email, generated_code)
        return BaseAccountsResponse.create(message="Код восстановления отправлен на почту")

    async def __validate_entity_by_email(self, email: str) -> None:
        entity = await self.__repository.filter_by(email=email)

        if not entity:
            raise AccountNotFoundError

        entity = entity[0]

        if not entity.is_active.value:
            raise AccountBadPermissionError

    async def __set_to_cache(self, email: str, code: Any) -> None:
        schema = RedisSchema.create(
            key=f"reset-pwd-{email}",
            value=code,
            ex=self.__settings.reset_pwd_code_lifetime
        )
        await self.__cache.set(schema)

    def __send_email_message(self, email: str, code: Any) -> None:
        message = self.__service.generate_simple_message(
            to=email,
            subject="Восстановление пароля",
            body=f"Ваш код для восстановления: {code}"
        )
        self.__service.send_email(message)

    @staticmethod
    def __generate_special_code() -> str:
        return str(random.randint(100000, 999999))
