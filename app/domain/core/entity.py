from dataclasses import dataclass
from typing import TypeVar, Generic

from app.domain.core.value_objects import ValueObject


EntityId = TypeVar("EntityId", bound=ValueObject)


@dataclass
class DomainEntity(Generic[EntityId]):
    id: EntityId
