import datetime as dt

from typing import Protocol


class IDateTimeProcessor(Protocol):
    def get_current_time(self) -> dt.datetime:
        raise NotImplementedError
