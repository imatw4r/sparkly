from typing import TypeVar

from pydantic.dataclasses import dataclass

from .mixins import DataclassAsDictMixin


@dataclass()
class Entity(DataclassAsDictMixin):
    """Base class for all entities."""


T_entity = TypeVar("T_entity", bound=Entity)
