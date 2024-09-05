from dataclasses import dataclass


@dataclass(frozen=True)
class ReactivationRequest:
    email: str
