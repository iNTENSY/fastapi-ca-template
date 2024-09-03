import os
from dataclasses import dataclass


@dataclass(frozen=True)
class RedisSettings:
    url: str
    encoding: str
    decode_responses: bool

    @staticmethod
    def from_env(encoding: str = "utf-8", decode_responses: bool = False) -> "RedisSettings":
        url = os.environ.get("REDIS_URL")

        if not url:
            raise RuntimeError("Missing REDIS_URL environment variable")

        return RedisSettings(url=url, encoding=encoding, decode_responses=decode_responses)
