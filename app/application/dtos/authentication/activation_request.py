from dataclasses import dataclass


@dataclass(frozen=True)
class ActivationRequest:
    email: str
    code: int
