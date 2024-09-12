import datetime as dt

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RedisSchema:
    """
    :param name: Ключ в хранилище
    :param value: Значение ключа
    :param ex: Срок действия в секундах. По стандарту отсутствует срок жизни.
    :param px: Срок действия в миллисекундах. По стандарту отсутствует срок жизни.
    :param nx: Указанная пара устанавливается только в том случае, когда данной пары не существует.
    :param xx: Указанная пара устанавливается только в том случае, когда она существует.
    :param keepttl: Если True, то сохраняет время жизни, связанное с ключом.
    """

    name: str
    value: Any
    ex: int | dt.timedelta | None = None
    px: int | dt.timedelta | None = None
    nx: bool = False
    xx: bool = False
    keepttl: bool = False

    @staticmethod
    def create(
            key: str,
            value: Any,
            *,
            ex: int | dt.timedelta | None = None,
            px: int | dt.timedelta | None = None,
            nx: bool = False,
            xx: bool = False,
            keepttl: bool = True,
    ) -> "RedisSchema":
        """Фабричный метод создания схемы для работы с Redis`ом."""
        return RedisSchema(name=key, value=value, ex=ex, px=px, nx=nx, xx=xx, keepttl=keepttl)
