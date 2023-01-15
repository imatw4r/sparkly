from typing import TypeVar

from pydantic import ConfigDict
from pydantic.dataclasses import dataclass

from .mixins import DataclassAsDictMixin


@dataclass(config=ConfigDict(use_enum_values=True, arbitrary_types_allowed=True))
class ValueObject(DataclassAsDictMixin):
    """Base class for value objects."""


T_value_object = TypeVar("T_value_object", bound=ValueObject)
