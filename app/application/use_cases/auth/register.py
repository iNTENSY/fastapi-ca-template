from sqlalchemy.exc import IntegrityError

from app.application.dtos.authentication.base_responses import RegistrationResponse
from app.application.dtos.authentication.register_request import RegistrationRequest
from app.application.interfaces.interactor import Interactor
from app.application.interfaces.password_hasher import IPasswordHasher
from app.application.interfaces.transaction_manager import ITransactionContextManager
from app.domain.accounts.entity import Account
from app.domain.accounts.repository import IAccountRepository
from app.domain.core import exceptions


class RegistrationUseCase(Interactor[RegistrationRequest, RegistrationResponse]):
    def __init__(
            self,
            repository: IAccountRepository,
            transaction_manager: ITransactionContextManager,
            pwd_hasher: IPasswordHasher
    ) -> None:
        self.__repository = repository
        self.__transaction = transaction_manager
        self.__pwd_hasher = pwd_hasher

    async def __call__(self, request: RegistrationRequest) -> RegistrationResponse:
        hashed_password = self.__pwd_hasher.hash_password(request.password)
        try:
            entity = Account.create(
                username=request.username,
                password=hashed_password,
                email=request.email,
            )
            await self.__repository.create(entity)
        except IntegrityError:
            await self.__transaction.rollback()
            raise exceptions.IntegrityError
        finally:
            await self.__transaction.commit()
        return RegistrationResponse.create(
            id=entity.id.value,
            username= entity.username.value,
            email= entity.email.value,
            is_verified=entity.is_verified.value
        )
