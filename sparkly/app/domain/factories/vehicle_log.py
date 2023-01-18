from typing import Any

from pydantic import BaseModel

from sparkly.app.seedwork import domain
from sparkly.app.seedwork.domain import exceptions

from .. import value_objects


class VehicleLogAttrs(BaseModel):
    timestamp: str
    speed: int | None
    odometer: float
    state_of_charge: int
    elevation: int
    shift_state: str | None

    class Config:
        orm_mode = True


class VehicleLog(
    domain.DomainFactory[
        VehicleLogAttrs,
        value_objects.VehicleLog,
    ],
):

    domain_class = value_objects.VehicleLog

    @classmethod
    def convert_attrs(cls, attrs: VehicleLogAttrs) -> dict[str, Any]:
        try:
            timestamp = value_objects.TimestampValue.fromisoformat(attrs.timestamp)
        except ValueError:
            raise exceptions.DomainValidationError(f"Invalid timestamp format: {attrs.timestamp!r}")

        speed = value_objects.VehicleSpeedValue(attrs.speed) if attrs.speed else None
        odometer = value_objects.OdometerValue(attrs.odometer)
        soc = value_objects.StateOfChargeValue(attrs.state_of_charge)
        elevation = value_objects.ElevationValue(attrs.elevation)
        state = value_objects.ShiftStateValue(attrs.shift_state) if attrs.shift_state else None
        shift_state = value_objects.ShiftStateValue(state) if state is not None else None

        log = cls.domain_class(
            timestamp=timestamp,
            speed=speed,
            odometer=odometer,
            state_of_charge=soc,
            elevation=elevation,
            shift_state=shift_state,
        )

        print(log.as_dict())

        return log.as_dict()
