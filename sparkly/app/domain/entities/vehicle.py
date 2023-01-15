import uuid

from pydantic import UUID4, Field

from sparkly.app.seedwork import domain

from ..value_objects import VehicleLog


class Vehicle(domain.Entity):
    id: UUID4
    data: list[VehicleLog] = Field(default_factory=list)

    @staticmethod
    def next_id() -> UUID4:
        return uuid.uuid4()
