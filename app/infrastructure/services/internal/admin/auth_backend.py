from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.application.interfaces.password_hasher import IPasswordHasher
from app.application.interfaces.redis import IRedis
from app.application.interfaces.session import ISessionProcessor
from app.domain.accounts.exceptions import AccountNotFoundError, InvalidUserDataError
from app.domain.accounts.repository import IAccountRepository


class AdminAuthBackend(AuthenticationBackend):
    def __init__(
            self,
            secret_key: str,
            redis: IRedis,
            session: ISessionProcessor,
            account_repository: IAccountRepository,
            pwd_hasher: IPasswordHasher
    ) -> None:
        super().__init__(secret_key)
        self.__redis = redis
        self.__session = session
        self.__repository = account_repository
        self.__pwd_hasher = pwd_hasher


    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        expected_account = await self.__repository.filter_by(username=username)
        if not expected_account:
            raise AccountNotFoundError
        if not self.__pwd_hasher.verify_password(password, expected_account[0].password.value):
            raise InvalidUserDataError

        session = await self.__session.generate_session(expected_account[0].id.value)
        request.session.update({"adm_session": session})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("adm_session")

        if not await self.__session.validate(token):
            return False
        return True
