from typing import TypeVar

import attrs


@attrs.define()
class Command:
    """Base class for a command."""


T_command = TypeVar("T_command", bound=Command)
