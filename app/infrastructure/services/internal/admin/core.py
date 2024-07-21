import os

from dishka import AsyncContainer
from fastapi import FastAPI
from sqladmin import Admin
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from app.application.interfaces.password_hasher import IPasswordHasher
from app.application.interfaces.redis import IRedis
from app.application.interfaces.session import ISessionProcessor
from app.domain.accounts.repository import IAccountRepository
from app.infrastructure.services.internal.admin.auth_backend import AdminAuthBackend
from app.infrastructure.services.internal.admin.pages import AccountAdmin
from app.infrastructure.settings.core import Settings


def init_sqladmin(app: FastAPI, container: AsyncContainer) -> None:
    """Admin integration."""

    with container() as app_container:
        engine = app_container.get(AsyncEngine)
        backend = AdminAuthBackend(
            secret_key=Settings.secret_key,
            redis=app_container.get(IRedis),
            session=app_container.get(ISessionProcessor),
            account_repository=app_container.get(IAccountRepository),
            pwd_hasher=app_container.get(IPasswordHasher),
        )

    admin = Admin(
        app,
        engine=engine,
        authentication_backend=backend
    )
    admin.add_view(AccountAdmin)
