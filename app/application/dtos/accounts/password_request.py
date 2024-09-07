from dataclasses import dataclass


@dataclass(frozen=True)
class ForgotPasswordRequest:
    email: str
