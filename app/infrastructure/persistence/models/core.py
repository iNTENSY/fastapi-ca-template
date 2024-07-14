import uuid
from typing import Annotated

from sqlalchemy import UUID
from sqlalchemy.orm import mapped_column, DeclarativeBase


intpk = Annotated[int, mapped_column(primary_key=True, index=True, nullable=False)]
uuidpk = Annotated[uuid.uuid4, mapped_column(UUID(as_uuid=True), primary_key=True, index=True, unique=True)] # noqa


class BaseModel(DeclarativeBase):
    pass
