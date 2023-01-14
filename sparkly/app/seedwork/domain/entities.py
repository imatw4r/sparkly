from typing import Any

from pydantic.dataclasses import dataclass


@dataclass
class Entity:
    """Base class for an entity."""

    id: Any

    @staticmethod
    def next_id() -> Any:
        raise NotImplementedError()
