from pydantic import UUID4

from sparkly.app.domain import queries, value_objects
from sparkly.app.seedwork import service_layer
from sparkly.app.seedwork.service_layer import mixins
from sparkly.app.service_layer import uow


class GetVehicleLogs(
    mixins.SQLAlchemyUnitOfWorkMixin[uow.VehicleUnitOfWork],
    service_layer.QueryHandler[queries.GetVehicleLogs, list[value_objects.VehicleLog]],
):
    async def __call__(
        self,
        query: queries.GetVehicleLogs,
    ) -> service_layer.HandlerResult[list[value_objects.VehicleLog]]:
        async with self.uow:
            logs = await self.uow.repository.get_logs(vehicle_id=query.vehicle_id)
            return service_layer.HandlerResult(result=logs)


class ListVehicles(
    mixins.SQLAlchemyUnitOfWorkMixin[uow.VehicleUnitOfWork],
    service_layer.QueryHandler[queries.ListVehicles, list[value_objects.VehicleLog]],
):
    async def __call__(
        self,
        query: queries.ListVehicles,
    ) -> service_layer.HandlerResult[list[UUID4]]:
        async with self.uow:
            vehicle_ids = await self.uow.repository.list_vehicles()
            return service_layer.HandlerResult(result=vehicle_ids)
