import os
from typing import Type

import pytest
import pytest_asyncio
from dotenv import load_dotenv
from httpx import AsyncClient, ASGITransport

from app.domain.accounts.entity import Account
from app.presentation.entrypoint import app_factory


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    app = app_factory()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture
def account_entity() -> Type[Account]:
    return Account
