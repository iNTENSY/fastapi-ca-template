import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class GetAccountRequest:
    uid: uuid.UUID
