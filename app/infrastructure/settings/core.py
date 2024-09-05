from dataclasses import dataclass

from app.infrastructure.settings.database import DatabaseSettings
from app.infrastructure.settings.jwt import JwtSettings
from app.infrastructure.settings.session import SessionSettings


@dataclass(frozen=True)
class Settings:
    secret_key: str
    activation_code_lifetime: int

    @staticmethod
    def create(
            secret_key: str,
            activation_code_lifetime: int
    ) -> "Settings":
        return Settings(
            secret_key=secret_key,
            activation_code_lifetime=activation_code_lifetime
        )
