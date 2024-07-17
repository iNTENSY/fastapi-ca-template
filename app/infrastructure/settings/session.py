import datetime as dt

from dataclasses import dataclass


@dataclass(frozen=True)
class SessionSettings:
    timedelta: int | dt.timedelta
