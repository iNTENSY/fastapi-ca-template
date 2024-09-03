from dishka import AsyncContainer
from fastapi import FastAPI
from sqladmin import Admin
from sqlalchemy.ext.asyncio import AsyncEngine

from app.application.interfaces.password_hasher import IPasswordHasher
from app.application.interfaces.redis import ICache
from app.application.interfaces.session import ISessionProcessor
from app.domain.accounts.repository import IAccountRepository
from app.infrastructure.services.internal.admin.auth_backend import AdminAuthBackend
from app.infrastructure.services.internal.admin.pages import AccountAdmin
from app.infrastructure.settings.core import Settings


async def init_sqladmin(app: FastAPI, container: AsyncContainer) -> None:
    """Admin integration."""
    async with container() as app_container:
        settings = await app_container.get(Settings)
        backend = AdminAuthBackend(
            secret_key=settings.secret_key,
            redis=await app_container.get(ICache),
            session=await app_container.get(ISessionProcessor),
            account_repository=await app_container.get(IAccountRepository),
            pwd_hasher=await app_container.get(IPasswordHasher),
        )
        admin = Admin(
            app,
            engine=await app_container.get(AsyncEngine),
            authentication_backend=backend
        )
        admin.add_view(AccountAdmin)
