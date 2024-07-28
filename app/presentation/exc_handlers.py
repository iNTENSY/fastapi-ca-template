from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.domain.accounts.exceptions import AccountNotFoundError
from app.domain.core.exceptions import DomainValidationError, InternalServerError


async def validation_error_exc_handler(request: Request, exc: DomainValidationError) -> JSONResponse:
    return JSONResponse(content={"detail": exc.message}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


async def internal_server_error_exc_handler(request: Request, exc: InternalServerError) -> JSONResponse:
    return JSONResponse(content={"detail": exc.message}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def account_not_found_error_exc_handler(request: Request, exc: AccountNotFoundError):
    return JSONResponse(content={"detail": exc.message}, status_code=status.HTTP_404_NOT_FOUND)


def init_exc_handlers(app: FastAPI):
    app.add_exception_handler(DomainValidationError, validation_error_exc_handler)
    app.add_exception_handler(InternalServerError, internal_server_error_exc_handler)
    app.add_exception_handler(AccountNotFoundError, account_not_found_error_exc_handler)
