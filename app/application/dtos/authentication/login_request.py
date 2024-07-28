from dataclasses import dataclass


@dataclass(frozen=True)
class LoginRequest:
    username: str
    password: str
