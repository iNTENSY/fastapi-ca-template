from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.infrastructure.di.providers.adapters import SQLAlchemyProvider, SettingsProvider, RedisProvider, \
    SessionProvider


def ioc_factory() -> AsyncContainer:
    return make_async_container(
        SQLAlchemyProvider(),
        SettingsProvider(),
        RedisProvider(),
        SessionProvider()
    )


def init_ioc(app: FastAPI) -> None:
    container = ioc_factory()
    setup_dishka(container, app)
