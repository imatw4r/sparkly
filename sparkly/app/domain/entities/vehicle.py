import uuid

from pydantic import UUID4, Field

from sparkly.app.domain import value_objects
from sparkly.app.seedwork import domain


class Vehicle(domain.Entity):
    id: UUID4
    data: list[value_objects.VehicleLog] = Field(default_factory=list)

    @staticmethod
    def next_id() -> UUID4:
        return uuid.uuid4()
