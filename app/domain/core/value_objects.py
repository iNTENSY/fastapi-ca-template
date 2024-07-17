import re
import uuid
from dataclasses import dataclass
from typing import TypeVar, Generic

from app.domain.core.exceptions import DomainValidationError


ValueT = TypeVar("ValueT")


@dataclass(frozen=True)
class ValueObject(Generic[ValueT]):
    value: ValueT

    def __post_init__(self) -> None:
        pass
        # self.validate()

    def validate(self) -> None:
        """
        Must be implemented by subclasses.
        Raises a :class:`DomainValidationError` if the value is invalid.
        """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value!r})"


@dataclass(frozen=True)
class IntegerVO(ValueObject):
    value: int

    def validate(self) -> None:
        if isinstance(self.value, bool) or not isinstance(self.value, int):
            raise DomainValidationError(message=f"Value ({self.value}) must be of type INTEGER")


@dataclass(frozen=True)
class PositiveIntegerVO(IntegerVO):
    def validate(self) -> None:
        super().validate()

        if self.value <= 0:
            raise DomainValidationError(message=f"Value ({self.value}) must be greater then 0")


@dataclass(frozen=True)
class FloatVO(ValueObject):
    value: float

    def validate(self) -> None:
        if not isinstance(self.value, float):
            raise DomainValidationError(message=f"Value ({self.value}) must be of type FLOAT")


@dataclass(frozen=True)
class PositiveFloatVO(FloatVO):
    def validate(self) -> None:
        super().validate()

        if self.value <= 0:
            raise DomainValidationError(message=f"Value ({self.value}) must be greater then 0")


@dataclass(frozen=True)
class UuidVO(ValueObject):
    value: uuid.UUID

    def validate(self) -> None:
        if isinstance(self.value, str) or not isinstance(self.value, uuid.UUID):
            raise DomainValidationError(message=f"Value ({self.value}) must be of type UUID")


@dataclass(frozen=True)
class BooleanVO(ValueObject):
    value: bool

    def validate(self) -> None:
        if not isinstance(self.value, bool):
            raise DomainValidationError(message=f"Value ({self.value}) must be of type BOOLEAN")


@dataclass(frozen=True)
class StringVO(ValueObject):
    value: str

    def validate(self) -> None:
        if not isinstance(self.value, str):
            raise DomainValidationError(message=f"Value ({self.value}) must be of type STRING")


@dataclass(frozen=True)
class DefaultIdVO(PositiveIntegerVO):
    """Should be used to implements positive integer ID."""


@dataclass(frozen=True)
class EmailVO(StringVO):
    def validate(self) -> None:
        super().validate()

        if "@" not in self.value:
            raise DomainValidationError(message=f"Value {self.value} must be EMAIL")


@dataclass(frozen=True)
class PhoneNumberVO(StringVO):
    def validate(self) -> None:
        pattern = r'^\+[0-9]{11}$'
        if not re.match(pattern, self.value):
            raise DomainValidationError(
                message="Incorrect phone number pattern",
            )