from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.infrastructure.di.providers.adapters import SQLAlchemyProvider, SettingsProvider, RedisProvider, \
    SessionProvider
from app.infrastructure.di.providers.use_cases import UseCasesProvider, RepositoriesProvider


def ioc_factory() -> AsyncContainer:
    return make_async_container(
        # Providers
        SQLAlchemyProvider(),
        SettingsProvider(),
        RedisProvider(),
        SessionProvider(),

        # Use cases and repositories
        RepositoriesProvider(),
        UseCasesProvider()
    )


def init_ioc(app: FastAPI) -> None:
    container = ioc_factory()
    setup_dishka(container, app)
