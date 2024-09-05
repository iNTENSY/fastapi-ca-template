from dataclasses import dataclass


@dataclass(frozen=True)
class RedisSettings:
    url: str
    encoding: str
    decode_responses: bool

    @staticmethod
    def from_env(url, encoding: str = "utf-8", decode_responses: bool = False) -> "RedisSettings":
        return RedisSettings(url=url, encoding=encoding, decode_responses=decode_responses)
