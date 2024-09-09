from app.application.dtos.accounts.base_responses import AccountResponse
from app.application.dtos.authentication.login_request import LoginRequest
from app.application.interfaces.interactor import Interactor
from app.application.interfaces.password_hasher import IPasswordHasher
from app.domain.accounts.entity import Account
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
        entity = await self.__get(username=request.username)
        self.__verify_password(request.password, entity.password.value)
        return AccountResponse.create(entity)

    async def __get(self, username: str) -> Account:
        entity = await self.__repository.filter_by(username=username)
        if not entity:
            raise AccountNotFoundError
        return entity[0]

    def __verify_password(self, password: str, expected_password: str) -> None:
        if not self.__pwd_hasher.verify_password(password, expected_password):
            raise InvalidAccountDataError
