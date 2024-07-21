import os
from dataclasses import dataclass


@dataclass(frozen=True)
class DatabaseSettings:
    db_url: str

    @staticmethod
    def from_env() -> "DatabaseSettings":
        url = os.getenv("DATABASE_URL")

        if not url:
            raise RuntimeError("Missing DATABASE_URL environment variable")

        return DatabaseSettings(url)
