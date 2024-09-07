from typing import Any, Tuple

import pytest

from app.domain.accounts.entity import Account
from app.domain.accounts.value_objects import UsernameVO
from app.domain.core.value_objects import UuidVO, EmailVO, StringVO, BooleanVO
from tests.unit.domain.core import _TestModelAttr


@pytest.mark.parametrize(
    "field, _type",
    (
            ("id", UuidVO),
            ("username", UsernameVO),
            ("email", EmailVO),
            ("password", StringVO),
            ("is_verified", BooleanVO),
            ("is_active", BooleanVO),
            ("is_staff", BooleanVO),
            ("is_superuser", BooleanVO),
    )
)
class Test01AccountEntity(_TestModelAttr):
    @property
    def model(self):
        return Account


class Test02AccountBaseAction:
    @staticmethod
    def check_expected_entity_fields(account: Account, expected_fields: dict[str, Any]) -> None:
        for attr, expected_result in expected_fields.items():
            value_object = getattr(account, attr)
            assert value_object.value == expected_result

    def test_to_create_entity_with_valid_data(self) -> None:
        account = Account.create(
            username="test",
            email="email@mail.ru",
            password="<PASSWORD>",
        )

        assert account.id is not None
        self.check_expected_entity_fields(account, {
            "is_active": True,
            "is_verified": False,
            "is_staff": False,
            "is_superuser": False
        })

    def test_to_update_entity_with_valid_data(self) -> None:
        account = Account.create(
            username="test",
            email="email@mail.ru",
            password="<PASSWORD>",
        )

        data_for_update = {
            "username": "NewUsername",
            "email": "new_email@mail.ru",
            "is_verified": True,
            "is_superuser": True,
        }

        account.update(**data_for_update)

        self.check_expected_entity_fields(account, data_for_update)
