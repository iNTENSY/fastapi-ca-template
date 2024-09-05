from dataclasses import dataclass

from app.infrastructure.settings.database import DatabaseSettings
from app.infrastructure.settings.jwt import JwtSettings
from app.infrastructure.settings.session import SessionSettings


@dataclass(frozen=True)
class Settings:
    secret_key: str

    @staticmethod
    def create(
            secret_key: str
    ) -> "Settings":
        return Settings(
            secret_key=secret_key
        )
