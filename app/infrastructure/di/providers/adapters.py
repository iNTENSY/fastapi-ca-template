import os
from typing import AsyncIterable

from redis import asyncio as aioredis
from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine, async_sessionmaker

from app.application.interfaces.email import IEmailService
from app.application.interfaces.jwt import IJwtProcessor
from app.application.interfaces.password_hasher import IPasswordHasher
from app.application.interfaces.redis import ICache
from app.application.interfaces.session import ISessionProcessor
from app.application.interfaces.timezone import IDateTimeProcessor
from app.application.interfaces.transaction_manager import ITransactionContextManager
from app.infrastructure.cache.redis_adapter import RedisAdapter
from app.infrastructure.persistence.transaction_manager import PostgreSQLTransactionContextManagerImp
from app.infrastructure.services.external.email.core import EmailServiceImp
from app.infrastructure.services.external.email.settings import EmailSettings
from app.infrastructure.services.internal.authentication.jwt import JwtProcessor
from app.infrastructure.services.internal.authentication.session import SessionProcessorImp
from app.infrastructure.services.internal.datetimes.timezone import SystemDateTimeProvider, Timezone
from app.infrastructure.services.internal.security.password_hasher import PasswordHasherImp
from app.infrastructure.settings.core import Settings
from app.infrastructure.settings.database import DatabaseSettings
from app.infrastructure.settings.jwt import JwtSettings
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


class TransactionManagerProvider(Provider):
    scope = Scope.REQUEST
    _manager = provide(PostgreSQLTransactionContextManagerImp, provides=ITransactionContextManager)


class SettingsProvider(Provider):
    @provide(scope=Scope.APP, provides=SessionSettings)
    def provide_session_settings(self) -> SessionSettings:
        timedelta_into_seconds = 3600
        return SessionSettings.create(timedelta_into_seconds)

    @provide(scope=Scope.APP, provides=JwtSettings)
    def provide_jwt_settings(self) -> JwtSettings:
        secret_key = os.environ.get("SECRET_KEY")
        expires_in = 30 * 60
        algorithm = "HS256"
        return JwtSettings.create(secret=secret_key, expires_in=expires_in, algorithm=algorithm)

    @provide(scope=Scope.APP, provides=Settings)
    def provide_project_settings(
            self,
            db: DatabaseSettings,
            session: SessionSettings,
            jwt: JwtSettings
    ) -> Settings:
        secret_key = os.environ.get("SECRET_KEY")
        return Settings.create(secret_key, db=db, session=session, jwt=jwt)


class RedisProvider(Provider):
    @provide(scope=Scope.APP, provides=RedisSettings)
    def provide_settings(self) -> RedisSettings:
        return RedisSettings.from_env(decode_responses=True)

    @provide(scope=Scope.APP, provides=ICache)
    async def provide_redis(self, settings: RedisSettings) -> ICache:
        aior = aioredis.from_url(settings.url, encoding=settings.encoding, decode_responses=settings.decode_responses)
        return RedisAdapter(aior)


class SessionProvider(Provider):
    @provide(scope=Scope.APP, provides=ISessionProcessor)
    async def provide_session(self, redis: ICache, settings: SessionSettings) -> ISessionProcessor:
        return SessionProcessorImp(redis, settings)


class SecurityHasher(Provider):
    scope = Scope.APP
    _app = provide(PasswordHasherImp, provides=IPasswordHasher)


class TimezoneProvider(Provider):
    @provide(scope=Scope.APP, provides=IDateTimeProcessor)
    def provide_timezone(self) -> SystemDateTimeProvider:
        return SystemDateTimeProvider(Timezone.MSK)


class JwtProvider(Provider):
    @provide(scope=Scope.APP, provides=IJwtProcessor)
    def provide_jwt_processor(self, settings: JwtSettings, dt: IDateTimeProcessor) -> IJwtProcessor:
        return JwtProcessor(settings, dt)


class EmailProvider(Provider):
    @provide(scope=Scope.APP, provides=EmailSettings)
    def provide_email_settings(self) -> EmailSettings:
        host = os.environ.get("EMAIL_HOST")
        port = os.environ.get("EMAIL_PORT")
        login = os.environ.get("EMAIL_LOGIN")
        password = os.environ.get("EMAIL_PASSWORD")
        return EmailSettings.create(host, int(port), login, password)

    @provide(scope=Scope.REQUEST, provides=IEmailService)
    async def provide_service(self, settings: EmailSettings) -> IEmailService:
        return EmailServiceImp(settings)
