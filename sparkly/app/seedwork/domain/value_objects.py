from pydantic import ConfigDict
from pydantic.dataclasses import dataclass


@dataclass(frozen=True, config=ConfigDict(use_enum_values=True))
class ValueObject:
    """Base class for value objects."""
