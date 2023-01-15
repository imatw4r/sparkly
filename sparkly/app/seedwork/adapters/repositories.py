import abc
from typing import Any, Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from ..domain import Entity

T_entity = TypeVar("T_entity", bound=Entity)

UUID = str


class Repository(abc.ABC, Generic[T_entity]):
    """Base class for repository representing a basic CRUD operations."""

    @abc.abstractmethod
    async def delete(self, id_: UUID) -> T_entity:
        """Delete object by id."""

    @abc.abstractmethod
    async def update(self, entity: T_entity, fields: dict[str, Any]) -> T_entity:
        """Update object."""

    @abc.abstractmethod
    async def create(self, entity: T_entity) -> T_entity:
        """Create object."""


T_repo = TypeVar("T_repo", bound=Repository)


class SQLAlchemyRepository(Repository[T_entity], Generic[T_entity]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
