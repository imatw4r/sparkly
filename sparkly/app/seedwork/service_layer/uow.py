from __future__ import annotations

import abc
from types import TracebackType
from typing import Generic, Optional, Type, TypeVar

from sqlalchemy.orm import sessionmaker

from sparkly.app.seedwork import adapters


class UnitOfWork(abc.ABC, Generic[adapters.T_repository]):
    """Base unit of work class."""

    @abc.abstractmethod
    async def __aenter__(self: UnitOfWork) -> UnitOfWork:
        ...

    @abc.abstractmethod
    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        ...


class SQLAlchemyUnitOfWork(UnitOfWork[adapters.T_sqlalchemy_repository], Generic[adapters.T_sqlalchemy_repository]):
    def __init__(self, session_factory: sessionmaker) -> None:
        self.factory = session_factory

    @property
    @abc.abstractmethod
    def repository_cls(self) -> Type[adapters.T_sqlalchemy_repository]:
        ...

    async def commit(self) -> None:
        if self.session:
            await self.session.commit()

    async def rollback(self) -> None:
        if self.session:
            await self.session.rollback()

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        if not self.session:
            return None

        if exc:
            await self.session.rollback()

        await self.session.close()

    async def __aenter__(self: SQLAlchemyUnitOfWork) -> SQLAlchemyUnitOfWork:
        self.session = self.factory()
        self.repository: adapters.T_sqlalchemy_repository = self.repository_cls(self.session)
        return self


T_sqlalchemy_uow = TypeVar("T_sqlalchemy_uow", bound=SQLAlchemyUnitOfWork)
