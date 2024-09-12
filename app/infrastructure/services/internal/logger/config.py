from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class LoggerSettings:
    level: Any
    name: str
    filename: str

    @staticmethod
    def create(level: Any, name: str, filename: str) -> 'LoggerSettings':
        return LoggerSettings(level, name, filename)
