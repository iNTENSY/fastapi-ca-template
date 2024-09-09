import random
from typing import Any

from sqlalchemy.exc import IntegrityError

from app.application.dtos.authentication.base_responses import RegistrationResponse
from app.application.dtos.authentication.register_request import RegistrationRequest
from app.application.interfaces.email import IEmailService
from app.application.interfaces.interactor import Interactor
from app.application.interfaces.password_hasher import IPasswordHasher
from app.application.interfaces.cache import ICache
from app.application.interfaces.transaction_manager import ITransactionContextManager
from app.domain.accounts.entity import Account
from app.domain.accounts.repository import IAccountRepository
from app.domain.core import exceptions
from app.infrastructure.cache.schema import RedisSchema
from app.infrastructure.services.internal.security.password_validator import PasswordValidator
from app.infrastructure.settings.core import Settings


class RegistrationUseCase(Interactor[RegistrationRequest, RegistrationResponse]):
    def __init__(
            self,
            repository: IAccountRepository,
            cache: ICache,
            transaction_manager: ITransactionContextManager,
            pwd_hasher: IPasswordHasher,
            pwd_validator: PasswordValidator,
            settings: Settings,
            email_service: IEmailService
    ) -> None:
        self.__repository = repository
        self.__cache = cache
        self.__transaction = transaction_manager
        self.__pwd_hasher = pwd_hasher
        self.__pwd_validator = pwd_validator
        self.__settings = settings
        self.__service = email_service

    async def __call__(self, request: RegistrationRequest) -> RegistrationResponse:
        self.__pwd_validator.validate(request.password)
        hashed_password = self.__pwd_hasher.hash_password(request.password)

        try:
            entity = await self.__create(request, hashed_password)
        except (IntegrityError, Exception):
            await self.__transaction.rollback()
            raise exceptions.IntegrityError
        finally:
            await self.__transaction.commit()

        generated_code = self.__generate_special_code()
        await self.__set_to_cache(request.email, generated_code)
        self.__send_email_message(request.email, generated_code)

        return RegistrationResponse.create(
            id=entity.id.value,
            username=entity.username.value,
            email=entity.email.value,
            is_verified=entity.is_verified.value
        )

    async def __create(self, request: RegistrationRequest, hashed_password: str) -> Account:
        entity = Account.create(
            username=request.username,
            password=hashed_password,
            email=request.email,
        )
        await self.__repository.create(entity)
        return entity

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
    def __generate_special_code() -> str:
        """
        Перепишите метод для генерации кода, на основе ваших требований.
        В данном же методе генерируется строка из случайного числа от 100 000 до 999 999.

        Метод должен возвращать строку, иначе если вы будете переопределять тип возвращаемых данных
        вам потребуется проверить корректность работы эндпоинта активации аккаунта.
        """
        return str(random.randint(100000, 999999))
