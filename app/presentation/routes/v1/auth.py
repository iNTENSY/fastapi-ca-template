from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from fastapi.responses import Response
from starlette.requests import Request

from app.application.dtos.authentication.activation_request import ActivationRequest
from app.application.dtos.authentication.base_responses import LoginResponse, RegistrationResponse, LogoutResponse, \
    ActivationResponse
from app.application.dtos.authentication.login_request import LoginRequest
from app.application.dtos.authentication.reactivation_request import ReactivationRequest
from app.application.dtos.authentication.register_request import RegistrationRequest
from app.application.interfaces.jwt import IJwtProcessor
from app.application.use_cases.auth.activation import ActivationUseCase
from app.application.use_cases.auth.login import LoginUseCase
from app.application.use_cases.auth.reactivation import ReactivationUseCase
from app.application.use_cases.auth.register import RegistrationUseCase
from app.infrastructure.services.internal.limiter.core import limiter

router = APIRouter(prefix="/auth", route_class=DishkaRoute)


@router.post("/login", response_model=LoginResponse)
async def login(
        request: LoginRequest,
        response: Response,
        interactor: FromDishka[LoginUseCase],
        jwt_processor: FromDishka[IJwtProcessor]
) -> LoginResponse:
    auth_response = await interactor(request)
    token = jwt_processor.generate_token(auth_response.uid, auth_response.email)
    response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)
    return LoginResponse(token)


@router.post("/register", response_model=RegistrationResponse)
async def register(
        request: RegistrationRequest,
        interactor: FromDishka[RegistrationUseCase]
) -> RegistrationResponse:
    return await interactor(request)


@router.get("/logout", response_model=LogoutResponse)
async def logout(response: Response) -> LogoutResponse:
    response.delete_cookie(key="access_token")
    return LogoutResponse(status="Logout successfully")


@router.get("/activate", response_model=ActivationResponse)
async def activate(
        request: Annotated[ActivationRequest, Depends()],
        interactor: FromDishka[ActivationUseCase]
) -> ActivationResponse:
    return await interactor(request)


@router.get("/reactivate", response_model=ActivationResponse)
@limiter.limit("3/hour")
async def reactivate(
        request: Request,
        _request: Annotated[ReactivationRequest, Depends()],
        interactor: FromDishka[ReactivationUseCase]
) -> ActivationResponse:
    return await interactor(_request)
