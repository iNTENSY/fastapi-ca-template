from dataclasses import dataclass


@dataclass(frozen=True)
class RegistrationRequest:
    username: str
    email: str
    password: str
