import asyncio
import os
from typing import Type, AsyncIterable, Generator

import pytest
from httpx import AsyncClient, ASGITransport
from sqladmin import Admin
from sqlalchemy import create_engine, QueuePool, insert, text, event
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine, \
    async_scoped_session

from app.domain.accounts.entity import Account
from app.infrastructure.persistence.mappers.account import AccountMapper
from app.infrastructure.persistence.models import AccountModel
from app.infrastructure.persistence.repositories.account import AccountRepositoryImp
from app.infrastructure.services.internal.security.password_hasher import PasswordHasherImp
from app.presentation.entrypoint import app_factory
from app.infrastructure.persistence.models.core import BaseModel


_data_base_url = os.environ.get('DATABASE_URL')


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
async def async_client() -> AsyncClient:
    app = app_factory()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture
async def admin_client(admin_entity) -> AsyncClient:
    app = app_factory()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        await client.post(
            "/api/v1/auth/login",
            json={
                "username": admin_entity.username.value,
                "password": "<PASSWORD>"
            }
        )
        assert client.cookies["access_token"]
        yield client


@pytest.fixture(scope="session", autouse=True)
def engine() -> AsyncEngine:
    return create_async_engine(_data_base_url)


@pytest.fixture(scope='session', autouse=True)
async def prepare_database(engine):
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)


@pytest.fixture
async def active_session(engine) -> AsyncSession:
    session = async_sessionmaker(bind=engine)
    async with session() as s:
        yield s


@pytest.fixture(scope="function", autouse=True)
async def teardown_function(active_session) -> None:
    await active_session.execute(text("DELETE FROM accounts"))
    await active_session.commit()


@pytest.fixture
async def admin_entity(active_session) -> Account:
    hashed_password = PasswordHasherImp.hash_password("<PASSWORD>")
    entity = Account.create(
        username='admin',
        password=hashed_password,
        email='email@mail.ru',
    )
    repository = AccountRepositoryImp(active_session)
    await repository.create(entity)
    await active_session.commit()
    return entity
