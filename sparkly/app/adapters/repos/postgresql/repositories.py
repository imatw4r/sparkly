from pydantic import UUID4
from sqlalchemy import insert

from sparkly.app.adapters.db.postgres import models
from sparkly.app.domain import entities, value_objects
from sparkly.app.seedwork import adapters


class VehicleRepository(adapters.SQLAlchemyRepository[entities.Vehicle]):
    async def add_log(self, vehicle_id: UUID4, log: value_objects.VehicleLog) -> None:
        stmnt = insert(models.vehicle_logs).values(
            vehicle_id=str(vehicle_id),
            timestamp=log.timestamp.value,
            speed=log.speed.value,
            speed_unit=log.speed.unit,
            odometer=log.odometer.value,
            odometer_unit=log.odometer.unit,
            state_of_charge=log.state_of_charge.value,
            elevation=log.elevation.value,
            elevation_unit=log.elevation.unit,
            shift_state=log.shift_state.value,
        )
        await self.session.execute(stmnt)
