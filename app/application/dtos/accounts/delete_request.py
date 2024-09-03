import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class DeleteAccountRequest:
    uid: uuid.UUID
