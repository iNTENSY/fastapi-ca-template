from typing import Protocol


class IPasswordHasher(Protocol):
    @staticmethod
    def hash_password(password: str) -> str: ...

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool: ...
