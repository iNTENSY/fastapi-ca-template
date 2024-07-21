from dataclasses import dataclass

from app.infrastructure.settings.session import SessionSettings


@dataclass(frozen=True)
class Settings:
    secret_key: str
    session: SessionSettings

    @staticmethod
    def create(
            secret_key: str,
            session: SessionSettings
    ) -> "Settings":
        if not isinstance(session, SessionSettings):
            raise ValueError

        return Settings(
            secret_key=secret_key,
            session=session
        )
