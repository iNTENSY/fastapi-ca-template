from sqladmin import ModelView

from app.infrastructure.persistence.models import AccountModel


class AccountAdmin(ModelView, model=AccountModel):
    """Account`s page into admin."""
    column_list = [
        AccountModel.id,
        AccountModel.username,
        AccountModel.is_verified,
        AccountModel.is_active,
        AccountModel.is_staff,
        AccountModel.is_superuser
    ]
