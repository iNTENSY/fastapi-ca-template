from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.domain.accounts.exceptions import AccountNotFoundError, AccountIsNotAuthorizedError, InvalidTokenError, \
    ValidationAPIError, AccountBadPermissionError, CacheError, ActivationError
from app.domain.core.exceptions import DomainValidationError, InternalServerError, IntegrityError


async def validation_error_exc_handler(request: Request, exc: DomainValidationError) -> JSONResponse:
    return JSONResponse(content={"detail": exc.message}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


async def internal_server_error_exc_handler(request: Request, exc: InternalServerError) -> JSONResponse:
    return JSONResponse(content={"detail": exc.message}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def account_not_found_error_exc_handler(request: Request, exc: AccountNotFoundError):
    return JSONResponse(content={"detail": exc.message}, status_code=status.HTTP_404_NOT_FOUND)


async def user_is_not_authorized_error_exc_handler(request: Request, exc: AccountIsNotAuthorizedError):
    return JSONResponse(content={"detail": exc.message}, status_code=status.HTTP_401_UNAUTHORIZED)


async def invalid_token_error_exc_handler(request: Request, exc: InvalidTokenError):
    return JSONResponse(content={"detail": exc.message}, status_code=status.HTTP_400_BAD_REQUEST)


async def pwd_validation_error_exc_handler(request: Request, exc: ValidationAPIError):
    return JSONResponse(content={"detail": exc.message}, status_code=status.HTTP_400_BAD_REQUEST)


async def bad_permission_error_exc_handler(request: Request, exc: AccountBadPermissionError):
    return JSONResponse(content={"detail": exc.message}, status_code=status.HTTP_403_FORBIDDEN)


async def integrity_error_exc_handler(request: Request, exc: IntegrityError):
    return JSONResponse(content={"detail": exc.message}, status_code=status.HTTP_400_BAD_REQUEST)


async def cache_error_exc_handler(request: Request, exc: CacheError):
    return JSONResponse(content={"detail": exc.message}, status_code=status.HTTP_400_BAD_REQUEST)


async def activation_error_exc_handler(request: Request, exc: ActivationError):
    return JSONResponse(content={"detail": exc.message}, status_code=status.HTTP_400_BAD_REQUEST)


def init_exc_handlers(app: FastAPI):
    app.add_exception_handler(DomainValidationError, validation_error_exc_handler)
    app.add_exception_handler(InternalServerError, internal_server_error_exc_handler)
    app.add_exception_handler(AccountNotFoundError, account_not_found_error_exc_handler)
    app.add_exception_handler(AccountIsNotAuthorizedError, user_is_not_authorized_error_exc_handler)
    app.add_exception_handler(InvalidTokenError, invalid_token_error_exc_handler)
    app.add_exception_handler(ValidationAPIError, pwd_validation_error_exc_handler)
    app.add_exception_handler(AccountBadPermissionError, bad_permission_error_exc_handler)
    app.add_exception_handler(IntegrityError, integrity_error_exc_handler)
    app.add_exception_handler(CacheError, cache_error_exc_handler)
    app.add_exception_handler(ActivationError, activation_error_exc_handler)
