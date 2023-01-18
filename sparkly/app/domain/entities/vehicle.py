import uuid

from pydantic import UUID4
from pydantic.dataclasses import dataclass

from sparkly.app.domain import value_objects
from sparkly.app.seedwork import domain


@dataclass()
class Vehicle(domain.Entity):
    id: UUID4

    def __post_init__(self) -> None:
        self.logs: list[value_objects.VehicleLog] = []

    @staticmethod
    def next_id() -> UUID4:
        return uuid.uuid4()

    def add_logs(self, logs: list[value_objects.VehicleLog]) -> None:
        self.logs.extend(logs)
