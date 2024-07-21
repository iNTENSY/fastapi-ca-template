from dishka import AsyncContainer, make_async_container

from app.infrastructure.di.providers.adapters import SQLAlchemyProvider, SettingsProvider, RedisProvider


def ioc_factory() -> AsyncContainer:
    return make_async_container(
        SQLAlchemyProvider(),
        SettingsProvider(),
        RedisProvider()
    )
