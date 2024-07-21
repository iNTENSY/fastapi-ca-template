import datetime as dt

from dataclasses import dataclass


@dataclass(frozen=True)
class SessionSettings:
    timedelta: int | dt.timedelta

    @staticmethod
    def create(timedelta: int | dt.timedelta) -> "SessionSettings":
        if isinstance(timedelta, int):
            timedelta = dt.timedelta(seconds=timedelta)
        return SessionSettings(timedelta=timedelta)
