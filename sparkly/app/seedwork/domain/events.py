from typing import TypeVar

from pydantic import BaseModel


class DomainEvent(BaseModel):
    """Base class for all domain events."""


T_domain_event = TypeVar("T_domain_event", bound=DomainEvent)
