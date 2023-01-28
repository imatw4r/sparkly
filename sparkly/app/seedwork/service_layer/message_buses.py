from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import TypeVar

from pydantic import ConfigDict
from pydantic import Field
from pydantic.dataclasses import dataclass

from .. import domain
from .. import service_layer

T_message = TypeVar("T_message", bound=domain.Command | domain.Query)
T_handler = TypeVar("T_handler", bound=service_layer.CommandHandler | service_layer.QueryHandler)


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class MessageBus(ABC, Generic[T_message, T_handler]):
    handlers: dict[type[T_message], T_handler] = Field(
        default_factory=dict,
    )

    def get_handler(self, message: T_message) -> T_handler:
        message_class = message.__class__
        try:
            return self.handlers[message_class]  # type: ignore
        except KeyError:
            error_msg = f"Handler for message {message!r} doesn't exist."
            raise ValueError(error_msg)

    @abstractmethod
    async def handle(self, message: T_message) -> service_layer.HandlerResult:
        ...


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class CommandBus(MessageBus[domain.Command, service_layer.CommandHandler]):
    async def handle(self, message: domain.Command) -> service_layer.HandlerResult:
        handler = self.get_handler(message=message)
        return await handler(command=message)


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class QueryBus(MessageBus[domain.Query, service_layer.QueryHandler]):
    async def handle(self, message: domain.Query) -> service_layer.HandlerResult:
        handler = self.get_handler(message=message)
        return await handler(query=message)
