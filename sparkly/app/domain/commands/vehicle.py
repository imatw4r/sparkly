import attrs
from pydantic import UUID4

from sparkly.app.seedwork import domain


# Do not use domain value_objects.VehicleLog
# as business logic may evolve separately
@attrs.define()
class VehicleLog:
    vehicle_id: str
    timestamp: str
    speed: int | None
    odometer: float
    shift_state: str | None
    state_of_charge: int
    elevation: int


@attrs.define()
class AddVehicleLog(domain.Command):
    log: VehicleLog


@attrs.define()
class AddVehicleLogBatch(domain.Command):
    log: list[VehicleLog]


@attrs.define()
class AddVehicle(domain.Command):
    vehicle_id: UUID4
