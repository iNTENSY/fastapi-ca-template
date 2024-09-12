import random
from typing import Any

from app.application.dtos.authentication.base_responses import ActivationResponse
from app.application.dtos.authentication.reactivation_request import ReactivationRequest
from app.application.interfaces.email import IEmailService
from app.application.interfaces.interactor import Interactor
from app.application.interfaces.cache import ICache
from app.domain.accounts.entity import Account
from app.domain.accounts.exceptions import AccountNotFoundError, ActivationError
from app.domain.accounts.repository import IAccountRepository
from app.infrastructure.services.internal.cache.schema import RedisSchema
from app.infrastructure.settings.core import Settings


class ReactivationUseCase(Interactor[ReactivationRequest, ActivationResponse]):
    def __init__(
            self,
            repository: IAccountRepository,
            cache: ICache,
            settings: Settings,
            email_service: IEmailService
    ) -> None:
        self.__repository = repository
        self.__cache = cache
        self.__settings = settings
        self.__service = email_service

    async def __call__(self, request: ReactivationRequest) -> ActivationResponse:
        try:
            entity = await self.__get(email=request.email)
        except IndexError:
            raise AccountNotFoundError

        self.__validate_entity(entity)
        generated_code = self.__generate_special_code()
        await self.__set_to_cache(request.email, generated_code)
        self.__send_email_message(request.email, generated_code)

        return ActivationResponse.create(message="Код активации отправлен на указанную почта")

    async def __get(self, email: str) -> Account:
        entity = await self.__repository.filter_by(email=email)
        return entity[0]

    async def __set_to_cache(self, email: str, code: Any) -> None:
        schema = RedisSchema.create(
            key=f"activation-{email}",
            value=code,
            ex=self.__settings.activation_code_lifetime
        )
        await self.__cache.set(schema)

    def __send_email_message(self, email: str, code: Any) -> None:
        message = self.__service.generate_simple_message(
            to=email,
            subject="Активация аккаунта",
            body=f"Ваш код активации {code}"
        )
        self.__service.send_email(message)

    @staticmethod
    def __validate_entity(entity: Account) -> None:
        if entity.is_verified:
            raise ActivationError("Аккаунт уже активирован")

        if not entity.is_active:
            raise ActivationError("Аккаунт заблокирован")

    @staticmethod
    def __generate_special_code() -> str:
        """
        Перепишите метод для генерации кода, на основе ваших требований.
        В данном же методе генерируется строка из случайного числа от 100 000 до 999 999.

        Метод должен возвращать строку, иначе если вы будете переопределять тип возвращаемых данных
        вам потребуется проверить корректность работы эндпоинта активации и реактивации аккаунта.
        """
        return str(random.randint(100000, 999999))
