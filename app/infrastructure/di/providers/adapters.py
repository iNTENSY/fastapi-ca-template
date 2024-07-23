from typing import AsyncIterable

from redis import asyncio as aioredis
from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine, async_sessionmaker

from app.application.interfaces.redis import IRedis
from app.application.interfaces.session import ISessionProcessor
from app.infrastructure.cache.redis_adapter import RedisAdapter
from app.infrastructure.services.internal.authentication.session import SessionProcessorImp
from app.infrastructure.settings.core import Settings
from app.infrastructure.settings.database import DatabaseSettings
from app.infrastructure.settings.redis import RedisSettings
from app.infrastructure.settings.session import SessionSettings


class SQLAlchemyProvider(Provider):
    @provide(scope=Scope.APP, provides=DatabaseSettings)
    def provide_settings(self) -> DatabaseSettings:
        return DatabaseSettings.from_env()

    @provide(scope=Scope.APP, provides=AsyncEngine)
    def provide_engine(self, settings: DatabaseSettings) -> AsyncEngine:
        return create_async_engine(settings.db_url)

    @provide(scope=Scope.APP, provides=async_sessionmaker[AsyncSession])
    def provide_session_maker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def provide_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session


class SettingsProvider(Provider):
    @provide(scope=Scope.APP, provides=SessionSettings)
    def provide_session_settings(self) -> SessionSettings:
        timedelta_into_seconds = 3600
        return SessionSettings.create(timedelta_into_seconds)

    @provide(scope=Scope.APP, provides=Settings)
    def provide_project_settings(
            self,
            db: DatabaseSettings,
            session: SessionSettings
    ) -> Settings:
        secret_key = "JKGBHJBkjkhbgUIY*YUHg371245"
        return Settings.create(secret_key, db=db, session=session)


class RedisProvider(Provider):
    @provide(scope=Scope.APP, provides=RedisSettings)
    def provide_settings(self) -> RedisSettings:
        return RedisSettings.from_env(decode_responses=True)

    @provide(scope=Scope.APP, provides=IRedis)
    async def provide_redis(self, settings: RedisSettings) -> IRedis:
        aior = aioredis.from_url(settings.url, encoding=settings.encoding, decode_responses=settings.decode_responses)
        return RedisAdapter(aior)


class SessionProvider(Provider):
    @provide(scope=Scope.APP, provides=ISessionProcessor)
    async def provide_session(self, redis: IRedis, settings: SessionSettings) -> ISessionProcessor:
        return SessionProcessorImp(redis, settings)
