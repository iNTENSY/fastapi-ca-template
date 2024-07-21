import uvicorn

from fastapi import FastAPI

from app.infrastructure.di.core import ioc_factory
from app.infrastructure.services.internal.admin.core import init_sqladmin
from app.presentation.exc_handlers import init_exc_handlers
from app.presentation.routes.v1.router import v1_router


def init_routes(app: FastAPI) -> None:
    """Integrate existing routes."""
    app.include_router(v1_router)


def app_factory() -> FastAPI:
    """Application factory."""
    app = FastAPI()

    container = ioc_factory(app)
    init_sqladmin(app, container)
    init_routes(app)
    init_exc_handlers(app)

    return app


if __name__ == "__main__":
    uvicorn.run("app.web_api.entrypoint:app_factory", reload=True, factory=True)
