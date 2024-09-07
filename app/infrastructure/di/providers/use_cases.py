from dishka import Provider, provide, Scope

from app.application.use_cases.accounts.all import GetAccountsUseCase
from app.application.use_cases.accounts.delete import DeleteAccountUseCase
from app.application.use_cases.accounts.get import GetAccountByUidUseCase
from app.application.use_cases.accounts.update import UpdateAccountUseCase
from app.application.use_cases.auth.activation import ActivationUseCase
from app.application.use_cases.auth.login import LoginUseCase
from app.application.use_cases.auth.reactivation import ReactivationUseCase
from app.application.use_cases.auth.register import RegistrationUseCase
from app.domain.accounts.repository import IAccountRepository
from app.infrastructure.persistence.repositories.account import AccountRepositoryImp


class RepositoriesProvider(Provider):
    scope = Scope.REQUEST

    account = provide(AccountRepositoryImp, provides=IAccountRepository)


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    _get = provide(GetAccountByUidUseCase)
    _all = provide(GetAccountsUseCase)
    _delete = provide(DeleteAccountUseCase)
    _update = provide(UpdateAccountUseCase)

    _auth_login = provide(LoginUseCase)
    _auth_register = provide(RegistrationUseCase)
    _auth_activate = provide(ActivationUseCase)
    _auth_reactivate = provide(ReactivationUseCase)
