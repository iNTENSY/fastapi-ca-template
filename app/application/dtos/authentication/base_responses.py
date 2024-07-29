import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class LoginResponse:
    access_token: str


@dataclass(frozen=True)
class RegistrationResponse:
    id: uuid.UUID
    username: str
    email: str
    is_verified: bool

    @staticmethod
    def create(id: uuid.UUID, username: str, email: str, is_verified: bool) -> "RegistrationResponse":
        return RegistrationResponse(
            id=id, username=username, email=email, is_verified=is_verified
        )


@dataclass(frozen=True)
class LogoutResponse:
    status: str
