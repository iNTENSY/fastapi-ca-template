from dataclasses import dataclass


@dataclass(frozen=True)
class EmailSettings:
    host: str
    port: int
    login: str
    password: str

    @staticmethod
    def create(host: str,
               port: int,
               login: str,
               password: str) -> "EmailSettings":
        assert isinstance(host, str), "Email must be STRING type"
        assert isinstance(port, int), "Port must be INT type"
        assert isinstance(login, str), "Login must be STRING type"
        assert isinstance(password, str), "Password must be STRING type"

        return EmailSettings(
            host=host,
            port=port,
            login=login,
            password=password
        )
