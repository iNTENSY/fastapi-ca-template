from dataclasses import dataclass


@dataclass(frozen=True)
class JwtSettings:
    secret: str
    expires_in: int
    algorithm: str

    @staticmethod
    def create(
            secret,
            expires_in,
            algorithm
    ) -> "JwtSettings":
        return JwtSettings(
            secret=secret,
            expires_in=expires_in,
            algorithm=algorithm
        )
