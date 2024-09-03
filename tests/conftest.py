from typing import Type

import pytest

from app.domain.accounts.entity import Account


@pytest.fixture
def account_entity() -> Type[Account]:
    return Account
