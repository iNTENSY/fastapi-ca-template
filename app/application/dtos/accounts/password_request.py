from dataclasses import dataclass


@dataclass(frozen=True)
class ForgotPasswordRequest:
    email: str


@dataclass(frozen=True)
class ResetPasswordRequest:
    code: str
    email: str
    password: str
