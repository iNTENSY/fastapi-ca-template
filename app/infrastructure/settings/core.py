from dataclasses import dataclass

from app.infrastructure.settings.database import DatabaseSettings
from app.infrastructure.settings.jwt import JwtSettings
from app.infrastructure.settings.session import SessionSettings


@dataclass(frozen=True)
class Settings:
    secret_key: str
    session: SessionSettings
    db: DatabaseSettings
    jwt: JwtSettings

    @staticmethod
    def create(
            secret_key: str,
            session: SessionSettings,
            db: DatabaseSettings,
            jwt: JwtSettings,
    ) -> "Settings":
        if not isinstance(session, SessionSettings):
            raise RuntimeError
        if not isinstance(db, DatabaseSettings):
            raise RuntimeError
        if not isinstance(jwt, JwtSettings):
            raise RuntimeError

        return Settings(
            secret_key=secret_key,
            session=session,
            db=db,
            jwt=jwt
        )
