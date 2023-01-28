from typing import Any

from fastapi_pagination import Page
from fastapi_pagination.ext.async_sqlalchemy import paginate
from pydantic import UUID4
from sqlalchemy import select

from sparkly.app.domain import entities
from sparkly.app.domain import value_objects
from sparkly.app.seedwork import adapters
from sparkly.app.seedwork.domain import exceptions


class VehicleNotFound(exceptions.DomainValidationError):
    def __init__(self, vehicle_id: UUID4) -> None:
        super().__init__("Vehicle not found.")
        self.vehicle_id = vehicle_id


class VehicleRepository(adapters.SQLAlchemyRepository[entities.Vehicle]):
    def paginate_query(self, query: Any) -> Any:
        return paginate(conn=self.session, query=query)

    async def get(self, id_: UUID4) -> entities.Vehicle | None:
        stmnt = select(entities.Vehicle).where(entities.Vehicle.id == id_)
        return await self.session.scalar(stmnt)

    async def add_log(self, log: value_objects.VehicleLog) -> None:
        vehicle = await self.get(id_=log.vehicle_id)
        if vehicle is None:
            raise VehicleNotFound(vehicle_id=log.vehicle_id)

        self.session.add(log)

    async def get_vehicle_logs(self, vehicle_id: UUID4) -> Page[value_objects.VehicleLog]:
        vehicle = await self.get(id_=vehicle_id)
        if not vehicle:
            raise VehicleNotFound(vehicle_id=vehicle_id)

        query = select(value_objects.VehicleLog).where(value_objects.VehicleLog.vehicle_id == vehicle_id)
        return self.paginate_query(query=query)

    async def list_vehicles(self) -> Page[entities.Vehicle]:
        query = select(entities.Vehicle)
        return self.paginate_query(query=query)
