from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.infrastructure.di.providers.adapters import SQLAlchemyProvider


def container_factory() -> AsyncContainer:
    return make_async_container(
        SQLAlchemyProvider()
    )


def ioc_factory(app: FastAPI) -> AsyncContainer:
    """Dishka`s integration."""
    container = container_factory()
    setup_dishka(container, app)
    return container
