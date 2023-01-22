from sqlalchemy import exc as db_exceptions

from sparkly.app.domain import commands, entities, factories
from sparkly.app.seedwork import service_layer
from sparkly.app.seedwork.service_layer import mixins
from sparkly.app.service_layer import uow

from .exceptions import VehicleAlreadyExists


class AddVehicleLog(
    mixins.SQLAlchemyUnitOfWorkMixin[uow.VehicleUnitOfWork], service_layer.CommandHandler[commands.AddVehicleLog]
):
    async def __call__(self, command: commands.AddVehicleLog) -> service_layer.HandlerResult[None]:
        attrs = factories.VehicleLogAttrs(
            vehicle_id=str(command.log.vehicle_id),
            timestamp=command.log.timestamp,
            speed=command.log.speed,
            odometer=command.log.odometer,
            shift_state=command.log.shift_state,
            state_of_charge=command.log.state_of_charge,
            elevation=command.log.elevation,
        )
        vehicle_log = factories.VehicleLog.create_from(attrs=attrs)
        async with self.uow:
            await self.uow.repository.add_log(log=vehicle_log)
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
            except db_exceptions.IntegrityError:
                raise VehicleAlreadyExists(vehicle_id=str(command.vehicle_id))
            return service_layer.HandlerResult(result=None)
