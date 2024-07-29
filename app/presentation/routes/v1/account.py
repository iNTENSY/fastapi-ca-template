from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends

from app.application.dtos.accounts.base_responses import AccountResponse, AccountsResponse
from app.application.dtos.accounts.get_request import GetAccountRequest, GetAccountsRequest
from app.application.use_cases.accounts.all import GetAccountsUseCase
from app.application.use_cases.accounts.get import GetAccountUseCase


router = APIRouter(prefix="/accounts", route_class=DishkaRoute)


@router.get("/", response_model=AccountsResponse)
async def find_all_accounts(
        request: Annotated[GetAccountsRequest, Depends()],
        interactor: FromDishka[GetAccountsUseCase]
) -> AccountsResponse:
    return await interactor(request)


@router.get("/{uid}", response_model=AccountResponse)
async def get_account_by_uid(
        request: Annotated[GetAccountRequest, Depends()],
        interactor: FromDishka[GetAccountUseCase]
) -> AccountResponse:
    return await interactor(request)
