from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from app.application.dtos.accounts.base_responses import AccountResponse
from app.application.dtos.accounts.get_request import GetAccountRequest
from app.application.use_cases.accounts.get import GetAccountUseCase


router = APIRouter(prefix="/accounts", route_class=DishkaRoute)


@router.get("/{uid}", response_model=AccountResponse)
async def get_account_by_uid(request: GetAccountRequest, interactor: FromDishka[GetAccountUseCase]):
    return interactor(request)
