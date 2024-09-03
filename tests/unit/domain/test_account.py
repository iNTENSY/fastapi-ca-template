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
