from __future__ import annotations

import abc
from types import TracebackType
from typing import Any, Coroutine, Optional, Type


class UnitOfWork(abc.ABC):
    """Base unit of work class."""

    @abc.abstractmethod
    def __enter__(self: UnitOfWork) -> UnitOfWork:
        ...

    @abc.abstractmethod
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Coroutine[Any, Any, None]:
        ...
