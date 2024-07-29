from app.application.interfaces.mapper import IMapper
from app.domain.accounts.entity import Account
from app.domain.core.value_objects import UuidVO, StringVO, EmailVO, BooleanVO


class AccountMapper(IMapper):
    @staticmethod
    def generate_to_entity(obj: dict, **inner_entities) -> Account:
        return Account(
            id=UuidVO(obj["id"]),
            username=StringVO(obj["username"]),
            email=EmailVO(obj["email"]),
            password=StringVO(obj["password"]),
            is_verified=BooleanVO(obj["is_verified"]),
            is_active=BooleanVO(obj["is_active"]),
            is_staff=BooleanVO(obj["is_staff"]),
            is_superuser=BooleanVO(obj["is_superuser"]),
        )
