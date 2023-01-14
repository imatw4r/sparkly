from typing import TypeVar

from pydantic import BaseModel


class Query(BaseModel):
    """Base class for all commands."""


T_query = TypeVar("T_query", bound=Query)
