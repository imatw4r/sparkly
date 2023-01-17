from typing import Any

from pydantic import BaseModel

from sparkly.app.seedwork import domain

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
        timestamp = value_objects.Timestamp(value=attrs.timestamp)
        speed = value_objects.VehicleSpeed(
            value=attrs.speed,
        )
        odometer = value_objects.Odometer(value=attrs.odometer)
        soc = value_objects.StateOfCharge(value=attrs.state_of_charge)
        elevation = value_objects.Elevation(value=attrs.elevation)
        state = value_objects.ShiftStateValue(attrs.shift_state) if attrs.shift_state else None
        shift_state = value_objects.ShiftState(value=state)
        return {
            "timestamp": timestamp,
            "speed": speed,
            "odometer": odometer,
            "state_of_charge": soc,
            "elevation": elevation,
            "shift_state": shift_state,
        }
