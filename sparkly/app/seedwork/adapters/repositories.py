import abc
from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from ..domain import Entity

T_entity = TypeVar("T_entity", bound=Entity)

UUID = str


class Repository(abc.ABC, Generic[T_entity]):
    """Base class for repository representing a basic operations."""

    @abc.abstractmethod
    async def delete(self, entity: T_entity) -> T_entity:
        """Delete object by id."""

    @abc.abstractmethod
    async def add(self, entity: T_entity) -> T_entity:
        """Add object."""


T_repository = TypeVar("T_repository", bound=Repository)


class SQLAlchemyRepository(Repository[T_entity], Generic[T_entity]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def add(self, entity: T_entity) -> T_entity:
        self.session.add(instance=entity)
        return entity

    async def delete(self, entity: T_entity) -> T_entity:
        await self.session.delete(entity)
        return entity


T_sqlalchemy_repository = TypeVar("T_sqlalchemy_repository", bound=SQLAlchemyRepository)
