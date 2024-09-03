import uuid
from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from app.application.dtos.accounts.base_responses import AccountResponse, AccountsResponse
from app.application.dtos.accounts.delete_request import DeleteAccountRequest
from app.application.dtos.accounts.get_request import GetAccountRequest, GetAccountsRequest
from app.application.interfaces.jwt import IJwtProcessor
from app.application.use_cases.accounts.all import GetAccountsUseCase
from app.application.use_cases.accounts.delete import DeleteAccountUseCase
from app.application.use_cases.accounts.get import GetAccountByUidUseCase
from app.domain.accounts.exceptions import InvalidTokenError
from app.infrastructure.services.internal.authentication.oauth2 import oauth2_scheme, auth_required

router = APIRouter(prefix="/accounts", route_class=DishkaRoute)


@router.get("/", response_model=AccountsResponse)
async def find_all_accounts(
        request: Annotated[GetAccountsRequest, Depends()],
        interactor: FromDishka[GetAccountsUseCase]
) -> AccountsResponse:
    return await interactor(request)


@router.get("/{uid:uuid}", response_model=AccountResponse)
async def get_account_by_uid(
        request: Annotated[GetAccountRequest, Depends()],
        interactor: FromDishka[GetAccountByUidUseCase]
) -> AccountResponse:
    return await interactor(request)


@router.get("/me", response_model=AccountResponse, dependencies=[Depends(auth_required)])
async def get_self_account(
        request: Request,
        interactor: FromDishka[GetAccountByUidUseCase],
        jwt_processor: FromDishka[IJwtProcessor]
) -> AccountResponse:
    token = request.scope["auth_token"]
    payload = jwt_processor.parse(token)
    if payload is None:
        raise InvalidTokenError
    response = await interactor(GetAccountRequest(uid=payload[0].value))
    return response


@router.delete("/", dependencies=[Depends(auth_required)])
async def delete_account_by_uid(
        request: Request,
        interactor: FromDishka[DeleteAccountUseCase],
        jwt_processor: FromDishka[IJwtProcessor]
):
    token = request.scope["auth_token"]
    payload = jwt_processor.parse(token)
    if payload is None:
        raise InvalidTokenError
    uid = payload[0].value
    await interactor(DeleteAccountRequest(uid=uid))
    return {"uid": uid}
