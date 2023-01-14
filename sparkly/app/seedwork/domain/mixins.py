from dataclasses import asdict
from typing import Any


class DataclassAsDictMixin:
    def as_dict(self) -> dict[str, Any]:
        return asdict(obj=self)
