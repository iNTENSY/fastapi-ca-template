import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class GetAccountRequest:
    uid: uuid.UUID


@dataclass(frozen=True)
class GetAccountsRequest:
    limit: int = 10
    offset: int = 0
