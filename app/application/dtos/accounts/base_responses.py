import uuid
from dataclasses import dataclass

from app.domain.accounts.entity import Account


@dataclass(frozen=True)
class AccountResponse:
    uid: uuid.UUID
    username: str
    email: str
    is_active: bool
    is_staff: bool
    is_superuser: bool

    @staticmethod
    def create(account: Account) -> "AccountResponse":
        return AccountResponse(
            uid=account.id.value,
            username=account.username.value,
            email=account.email.value,
            is_active=account.is_active.value,
            is_staff=account.is_staff.value,
            is_superuser=account.is_superuser.value,
        )


@dataclass(frozen=True)
class AccountsResponse:
    items: list[AccountResponse]
    count: int

    @staticmethod
    def create(accounts: list[Account]) -> "AccountsResponse":
        return AccountsResponse(
            items=[AccountResponse.create(account) for account in accounts],
            count=len(accounts)
        )


@dataclass(frozen=True)
class BaseAccountsResponse:
    message: str

    @staticmethod
    def create(message: str) -> "BaseAccountsResponse":
        return BaseAccountsResponse(message)
