from dishka import Provider, provide, Scope

from app.application.use_cases.accounts.get import GetAccountUseCase
from app.domain.accounts.repository import IAccountRepository
from app.infrastructure.persistence.repositories.account import AccountRepositoryImp


class RepositoriesProvider(Provider):
    scope = Scope.REQUEST

    account = provide(AccountRepositoryImp, provides=IAccountRepository)


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    get = provide(GetAccountUseCase)
