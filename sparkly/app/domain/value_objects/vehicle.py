from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING, TypeAlias

from pydantic import UUID4, condecimal, conint, root_validator
from pydantic.dataclasses import dataclass

from sparkly.app.seedwork import domain

if TYPE_CHECKING:
    StateOfChargeValue: TypeAlias = int
    OdometerValue: TypeAlias = Decimal
    VehicleSpeedValue: TypeAlias = int

else:
    StateOfChargeValue = conint(strict=True, ge=0)
    OdometerValue = condecimal(ge=Decimal(value=0))
    VehicleSpeedValue = conint(strict=True, ge=0)

TimestampValue: TypeAlias = datetime
ElevationValue: TypeAlias = int
VehicleIdValue: TypeAlias = UUID4


class ShiftStateValue(str, Enum):
    PARK = "P"
    REVERSE = "R"
    DRIVE = "D"


class VehicleSpeedUnitEnum(str, Enum):
    km_per_hour = "km/h"


class OdometerUnitEnum(str, Enum):
    km = "km"


class ElevationUnitEnum(str, Enum):
    meter = "m"


@dataclass()
class VehicleLog(domain.ValueObject):
    vehicle_id: VehicleIdValue
    timestamp: TimestampValue
    elevation: ElevationValue

    odometer: OdometerValue
    speed: VehicleSpeedValue | None
    state_of_charge: StateOfChargeValue
    shift_state: ShiftStateValue | None

    timestamp_format: str = "ISO8601"
    elevation_unit: ElevationUnitEnum = ElevationUnitEnum.meter
    odometer_unit: OdometerUnitEnum = OdometerUnitEnum.km
    speed_unit: VehicleSpeedUnitEnum | None = VehicleSpeedUnitEnum.km_per_hour

    @root_validator()
    def validate(cls, values):
        if values.get("shift_state") is None and values.get("speed") is not None:
            raise ValueError("Speed must be NULL when shift state is NULL")
        return values
