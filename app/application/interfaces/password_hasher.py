from typing import Protocol


class IPasswordHasher(Protocol):
    @staticmethod
    async def hash_password(password: str) -> str: ...

    @staticmethod
    async def verify_password(password: str, hashed_password: str) -> bool: ...
