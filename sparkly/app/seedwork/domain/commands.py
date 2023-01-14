from typing import TypeVar

from pydantic import BaseModel


class Command(BaseModel):
    """Base class for a command."""


T_command = TypeVar("T_command", bound=Command)
