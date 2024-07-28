import datetime as dt

from dataclasses import dataclass


@dataclass(frozen=True)
class JwtSettings:
    secret: str
    expires_in: int | dt.timedelta
    algorithm: str

    @staticmethod
    def create(
            secret,
            expires_in,
            algorithm
    ) -> "JwtSettings":
        if isinstance(expires_in, int):
            expires_in = dt.timedelta(seconds=expires_in)
        return JwtSettings(
            secret=secret,
            expires_in=expires_in,
            algorithm=algorithm
        )
