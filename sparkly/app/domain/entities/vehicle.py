import uuid

from pydantic import UUID4, Field
from pydantic.dataclasses import dataclass

from sparkly.app.domain import value_objects
from sparkly.app.seedwork import domain


@dataclass()
class Vehicle(domain.Entity):
    id: UUID4
    logs: list[value_objects.VehicleLog] = Field(default_factory=list)

    @staticmethod
    def next_id() -> UUID4:
        return uuid.uuid4()
