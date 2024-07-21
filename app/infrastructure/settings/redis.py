import os
from dataclasses import dataclass


@dataclass(frozen=True)
class RedisSettings:
    url: str

    @staticmethod
    def from_env() -> "RedisSettings":
        url = os.getenv("REDIS_URL")

        if not url:
            raise RuntimeError("Missing REDIS_URL environment variable")

        return RedisSettings(url)
