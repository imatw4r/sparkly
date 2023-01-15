from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

from .. import domain

# from ..domain import DomainEvent, T_command, T_domain_event, T_query

T_handler_result = TypeVar("T_handler_result")


class HandlerResult(BaseModel, Generic[T_handler_result]):
    result: T_handler_result
    # It might happen that a command results in domain events being created
    domain_events: list[domain.DomainEvent] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True


class CommandHandler(
    Generic[
        domain.T_command,
    ],
    ABC,
):
    @abstractmethod
    async def __call__(
        self,
        command: domain.T_command,
    ) -> Any:
        ...


T_command_handler = TypeVar("T_command_handler", bound=CommandHandler)