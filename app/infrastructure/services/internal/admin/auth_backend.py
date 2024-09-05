from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.application.interfaces.password_hasher import IPasswordHasher
from app.application.interfaces.redis import ICache
from app.application.interfaces.session import ISessionProcessor
from app.domain.accounts.exceptions import AccountNotFoundError, InvalidAccountDataError, UserBadPermissionError, \
    UserIsNotAuthorizedError
from app.domain.accounts.repository import IAccountRepository


class AdminAuthBackend(AuthenticationBackend):
    def __init__(
            self,
            secret_key: str,
            redis: ICache,
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
            return False

        account = expected_account[0]
        if not self.__pwd_hasher.verify_password(password, account.password.value):
            return False
        if not account.is_superuser.value:
            return False

        session = await self.__session.generate_session(account.id.value)
        request.session.update({"adm_session": session})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("adm_session")
        if not token:
            return False
        try:
            return bool(await self.__session.validate(token))
        except (UserIsNotAuthorizedError, Exception):
            return False
