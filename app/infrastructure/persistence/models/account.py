from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.persistence.models.core import BaseModel, uuidpk


class AccountModel(BaseModel):
    __tablename__ = "accounts"

    id: Mapped[uuidpk]
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_staff: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)
