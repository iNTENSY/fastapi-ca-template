from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI


def container_factory() -> AsyncContainer:
    return make_async_container()



def ioc_factory(app: FastAPI) -> AsyncContainer:
    """Dishka`s integration."""
    container = container_factory()
    setup_dishka(container, app)
    return container
