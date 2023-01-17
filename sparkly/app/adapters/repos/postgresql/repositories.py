from pydantic import UUID4
from sqlalchemy import select

from sparkly.app.domain import entities, value_objects
from sparkly.app.seedwork import adapters
from sparkly.app.seedwork.domain import exceptions


class VehicleNotFound(exceptions.DomainValidationError):
    def __init__(self, vehicle_id: UUID4) -> None:
        super().__init__("Vehicle not found.")
        self.vehicle_id = vehicle_id


class VehicleRepository(adapters.SQLAlchemyRepository[entities.Vehicle]):
    async def get(self, id_: UUID4) -> entities.Vehicle | None:
        stmnt = select(entities.Vehicle).where(entities.Vehicle.id == id_)
        result = await self.session.execute(stmnt)
        return result.scalar()

    async def add_log(self, vehicle_id: UUID4, log: value_objects.VehicleLog) -> None:
        vehicle = await self.get(id_=vehicle_id)
        if vehicle is None:
            raise VehicleNotFound(vehicle_id=vehicle_id)

        vehicle.add_logs([log])

    async def get_logs(self, vehicle_id: UUID4) -> list[value_objects.VehicleLog]:
        vehicle = await self.get(id_=vehicle_id)
        if not vehicle:
            raise VehicleNotFound(vehicle_id=vehicle_id)
        return vehicle.logs
