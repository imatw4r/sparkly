import attrs
from pydantic import UUID4

from sparkly.app.seedwork import domain


# Do not use domain value_objects.VehicleLog
# as business logic may evolve separately
@attrs.define()
class VehicleLog:
    timestamp: str
    speed: int | None
    odometer: float
    shift_state: str | None
    state_of_charge: int
    elevation: int


@attrs.define()
class AddVehicleLog(domain.Command):
    vehicle_id: UUID4
    log: VehicleLog
