from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    secret_key: str
    activation_code_lifetime: int

    @staticmethod
    def create(
            secret_key: str,
            activation_code_lifetime: int
    ) -> "Settings":
        return Settings(
            secret_key=secret_key,
            activation_code_lifetime=activation_code_lifetime
        )
