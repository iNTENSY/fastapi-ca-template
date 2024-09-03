import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class DatabaseSettings:
    db_url: str

    @staticmethod
    def from_env(url) -> "DatabaseSettings":
        return DatabaseSettings(url)
