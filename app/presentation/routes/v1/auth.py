from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi.responses import Response

from app.application.dtos.authentication.base_responses import LoginResponse
from app.application.dtos.authentication.login_request import LoginRequest
from app.application.interfaces.jwt import IJwtProcessor
from app.application.use_cases.auth.login import LoginUseCase


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
