from dataclasses import dataclass

from app.infrastructure.settings.session import SessionSettings


@dataclass(frozen=True)
class Settings:
    session: SessionSettings

    @staticmethod
    def create(
            session: SessionSettings
    ) -> "Settings":
        if not isinstance(session, SessionSettings):
            raise ValueError

        return Settings(
            session=session
        )
