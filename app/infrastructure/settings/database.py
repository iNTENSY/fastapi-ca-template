from dataclasses import dataclass


@dataclass(frozen=True)
class DatabaseSettings:
    db_url: str

    @staticmethod
    def from_env(url) -> "DatabaseSettings":
        return DatabaseSettings(url)
