from app.application.dtos.accounts.base_responses import AccountResponse
from app.application.dtos.authentication.login_request import LoginRequest
from app.application.interfaces.interactor import Interactor
from app.application.interfaces.password_hasher import IPasswordHasher
from app.domain.accounts.exceptions import AccountNotFoundError, InvalidAccountDataError
from app.domain.accounts.repository import IAccountRepository


class LoginUseCase(Interactor[LoginRequest, AccountResponse]):
    def __init__(
            self,
            repository: IAccountRepository,
            pwd_hasher: IPasswordHasher,
    ) -> None:
        self.__repository = repository
        self.__pwd_hasher = pwd_hasher

    async def __call__(self, request: LoginRequest) -> AccountResponse:
        entity = await self.__repository.filter_by(username=request.username)
        if not entity:
            raise AccountNotFoundError
        entity = entity[0]
        if not self.__pwd_hasher.verify_password(request.password, entity.password.value):
            raise InvalidAccountDataError
        return AccountResponse.create(entity)
