from pydantic import UUID4, Field
from pydantic.dataclasses import dataclass

from sparkly.app.domain import value_objects
from sparkly.app.seedwork import domain


@dataclass
class Vehicle(domain.Aggregate):
    id: UUID4
    logs: list[value_objects.VehicleLog] = Field(default_factory=list)

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if type(other) == type(self):
            return self.id == other.id  # type: ignore

        return False

    def add_logs(self, logs: list[value_objects.VehicleLog]) -> None:
        self.logs.extend(logs)
