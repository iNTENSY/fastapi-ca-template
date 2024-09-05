from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.infrastructure.di.providers.adapters import SQLAlchemyProvider, SettingsProvider, RedisProvider, \
    SessionProvider, SecurityHasher, TimezoneProvider, JwtProvider, EmailProvider, TransactionManagerProvider
from app.infrastructure.di.providers.use_cases import UseCasesProvider, RepositoriesProvider


def ioc_factory() -> AsyncContainer:
    return make_async_container(
        # Providers
        SQLAlchemyProvider(),
        TransactionManagerProvider(),
        SettingsProvider(),
        RedisProvider(),
        SessionProvider(),
        SecurityHasher(),
        TimezoneProvider(),
        JwtProvider(),

        # Use cases and repositories
        RepositoriesProvider(),
        UseCasesProvider(),

        # Services and other
        EmailProvider(),
    )


def init_ioc(app: FastAPI) -> None:
    container = ioc_factory()
    setup_dishka(container, app)
