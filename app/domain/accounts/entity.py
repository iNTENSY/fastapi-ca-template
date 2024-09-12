import uuid
from dataclasses import dataclass

from app.domain.accounts.value_objects import UsernameVO
from app.domain.core.entity import DomainEntity
from app.domain.core.value_objects import UuidVO, StringVO, EmailVO, BooleanVO, ValueObject


@dataclass
class Account(DomainEntity):
    id: UuidVO
    username: UsernameVO
    email: EmailVO
    password: StringVO
    is_verified: BooleanVO
    is_active: BooleanVO
    is_staff: BooleanVO
    is_superuser: BooleanVO

    @staticmethod
    def create(
            username: str,
            email: str,
            password: str,
            is_verified: bool = False,
            is_active: bool = True,
            is_staff: bool = False,
            is_superuser: bool = False
    ) -> "Account":
        return Account(
            id=UuidVO(uuid.uuid4()),
            username=UsernameVO(username),
            email=EmailVO(email),
            password=StringVO(password),
            is_verified=BooleanVO(is_verified),
            is_active=BooleanVO(is_active),
            is_staff=BooleanVO(is_staff),
            is_superuser=BooleanVO(is_superuser),
        )

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                attribute: ValueObject = getattr(self, key)
                value_object_type = attribute.__class__
            else:
                continue
            setattr(self, key, value_object_type(value))
