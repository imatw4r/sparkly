import abc
from typing import Any, Generic, TypeVar

from ..domain import Entity

T_entity = TypeVar("T_entity", bound=Entity)

UUID = str


class Repository(abc.ABC, Generic[T_entity]):
    """Base class for repository representing a basic CRUD operations."""

    @abc.abstractmethod
    def get(self, id_: UUID) -> T_entity:
        """Return object by id."""

    @abc.abstractmethod
    def delete(self, id_: UUID) -> None:
        """Delete object by id."""

    @abc.abstractmethod
    def update(self, entity: T_entity, fields: dict[str, Any]) -> T_entity:
        """Update object."""

    @abc.abstractmethod
    def create(self, entity: T_entity) -> T_entity:
        """Create object."""
