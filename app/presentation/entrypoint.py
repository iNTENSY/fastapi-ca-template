import os
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.application.interfaces.redis import IRedis
from app.infrastructure.di.core import init_ioc
from app.infrastructure.services.internal.admin.core import init_sqladmin
from app.presentation.exc_handlers import init_exc_handlers
from app.presentation.routes.v1.router import v1_router


load_dotenv("../../.env")


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    async with app.state.dishka_container() as app_container:
        redis_adapter = await app_container.get(IRedis)
        if not await redis_adapter.redis.ping():
            raise RuntimeError("Cant connect to redis. Application stopped")

    FastAPICache.init(RedisBackend(redis_adapter.redis), prefix="fastapi-cache")

    # Bad but ready-to-use implementation.
    # This implementation requires async/await to work with containers from IoC
    await init_sqladmin(app, app.state.dishka_container)

    # Todo: Must init rabbitmq after
    yield

    # RMQ must be closed there
    await redis_adapter.close()


def init_routes(app: FastAPI) -> None:
    """Integrate existing routes."""
    app.include_router(v1_router)


def app_factory() -> FastAPI:
    """Application factory."""
    app = FastAPI(debug=bool(os.environ.get("DEBUG")), lifespan=app_lifespan)

    init_ioc(app)
    init_routes(app)
    init_exc_handlers(app)
    return app


if __name__ == "__main__":
    uvicorn.run("app.presentation.entrypoint:app_factory", reload=True, factory=True)
