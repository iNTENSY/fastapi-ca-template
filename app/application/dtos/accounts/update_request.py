import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class UpdateRequest:
    uid: uuid.UUID
    username: str
    email: str
