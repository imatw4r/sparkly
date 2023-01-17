from sparkly.app.domain import queries
from sparkly.app.seedwork.service_layer import mixins
from sparkly.app.seedwork.service_layer.handlers import HandlerResult, QueryHandler
from sparkly.app.service_layer import uow
from sparkly.app.domain import value_objects


class GetVehicleLogs(
    mixins.SQLAlchemyUnitOfWorkMixin[uow.VehicleUnitOfWork],
    QueryHandler[queries.GetVehicleLogs, None],
):
    async def __call__(
        self,
        query: queries.GetVehicleLogs,
    ) -> HandlerResult[list[value_objects.VehicleLog]]:
        async with self.uow:
            logs = await self.uow.repository.get_logs(vehicle_id=query.vehicle_id)
            return HandlerResult(result=logs)
