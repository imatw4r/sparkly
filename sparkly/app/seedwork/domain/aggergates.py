from pydantic.dataclasses import dataclass

from .entities import Entity


@dataclass
class Aggregate(Entity):
    """Base class for an aggregate."""
