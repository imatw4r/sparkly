from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING, Any, TypeAlias

from pydantic import BaseModel, condecimal, conint, root_validator, validator
from pydantic.dataclasses import dataclass

from sparkly.app.seedwork import domain

if TYPE_CHECKING:
    StateOfChargeValue: TypeAlias = int
    OdometerValue: TypeAlias = Decimal
    VehicleSpeedValue: TypeAlias = int

else:
    StateOfChargeValue = conint(strict=True, ge=0)
    OdometerValue = condecimal(ge=Decimal(value=0), decimal_places=1)
    VehicleSpeedValue = conint(strict=True, ge=0)


class CustomType(BaseModel):
    """Base class for custom types."""

    value: Any

    class Config:
        use_enum_values = True
        frozen = True
        json_encoders = {datetime: lambda dt: str(dt)}


class Timestamp(CustomType):
    value: datetime

    @validator("value", pre=True)
    def transform_value(cls, value: str) -> datetime:
        return datetime.fromisoformat(value)


class StateOfCharge(CustomType):
    value: StateOfChargeValue


class ShiftStateValue(str, Enum):
    PARK = "P"
    REVERSE = "R"
    DRIVE = "D"


class ShiftState(CustomType):
    value: ShiftStateValue | None


class VehicleSpeedUnitEnum(str, Enum):
    km_per_hour = "km/h"


class VehicleSpeed(CustomType):
    value: VehicleSpeedValue | None
    unit: VehicleSpeedUnitEnum = VehicleSpeedUnitEnum.km_per_hour


class OdometerUnitEnum(str, Enum):
    km = "km"


class Odometer(CustomType):
    value: OdometerValue
    unit: OdometerUnitEnum = OdometerUnitEnum.km


class ElevationUnitEnum(str, Enum):
    meter = "m"


class Elevation(CustomType):
    value: int
    unit: ElevationUnitEnum = ElevationUnitEnum.meter


@dataclass(frozen=True)
class VehicleLog(domain.ValueObject):
    timestamp: Timestamp
    speed: VehicleSpeed
    odometer: Odometer
    shift_state: ShiftState
    state_of_charge: StateOfCharge
    elevation: Elevation

    @root_validator()
    def validate(cls, values):

        if values["shift_speed"].value is None and values["speed"].value is not None:
            raise ValueError("Speed must be NULL when shift state is NULL")
        return values
