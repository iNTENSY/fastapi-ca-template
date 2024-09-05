from typing import Protocol


class ILogger(Protocol):
    def debug(self, message: str) -> None:
        raise NotImplementedError

    def info(self, message: str) -> None:
        raise NotImplementedError

    def warning(self, message: str) -> None:
        raise NotImplementedError

    def error(self, message: str) -> None:
        raise NotImplementedError

    def critical(self, message: str) -> None:
        raise NotImplementedError
