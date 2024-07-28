from dataclasses import dataclass


@dataclass(frozen=True)
class LoginResponse:
    access_token: str
