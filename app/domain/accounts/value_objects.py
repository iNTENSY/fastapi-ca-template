from dataclasses import dataclass

from app.domain.core.exceptions import DomainValidationError
from app.domain.core.value_objects import StringVO


@dataclass(frozen=True)
class UsernameVO(StringVO):
    def validate(self) -> None:
        super().validate()

        if not self.value.isalpha():
            raise DomainValidationError("Username must have only alphabet letters.")

        if len(self.value) < 4:
            raise DomainValidationError("Username must be more than 4 characters.")
