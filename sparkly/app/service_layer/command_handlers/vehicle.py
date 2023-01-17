from sparkly.app.domain import commands, entities, factories
from sparkly.app.seedwork import service_layer
from sparkly.app.seedwork.service_layer import mixins
from sparkly.app.service_layer import uow


class AddVehicleLog(
    mixins.SQLAlchemyUnitOfWorkMixin[uow.VehicleUnitOfWork], service_layer.CommandHandler[commands.AddVehicleLog]
):
    async def __call__(self, command: commands.AddVehicleLog) -> service_layer.HandlerResult[None]:
        attrs = factories.VehicleLogAttrs(
            timestamp=command.log.timestamp,
            speed=command.log.speed,
            odometer=command.log.odometer,
            shift_state=command.log.shift_state,
            state_of_charge=command.log.state_of_charge,
            elevation=command.log.elevation,
        )
        vehicle_log = factories.VehicleLog.create_from(attrs=attrs)
        async with self.uow:
            await self.uow.repository.add_log(vehicle_id=command.vehicle_id, log=vehicle_log)
            await self.uow.commit()
            return service_layer.HandlerResult(result=None)


class AddVehicle(
    mixins.SQLAlchemyUnitOfWorkMixin[uow.VehicleUnitOfWork], service_layer.CommandHandler[commands.AddVehicle]
):
    async def __call__(self, command: commands.AddVehicle) -> service_layer.HandlerResult[None]:
        vehicle = entities.Vehicle(id=command.vehicle_id)

        async with self.uow:
            self.uow.repository.add(entity=vehicle)
            try:
                await self.uow.commit()
            except 
            return service_layer.HandlerResult(result=None)
