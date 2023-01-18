from pydantic import BaseModel, UUID4
from datetime import datetime
from decimal import Decimal


class VehicleLog(BaseModel):
    class Config:
        orm_mode = True

    timestamp: datetime
    elevation: int

    odometer: Decimal
    speed: str | None
    state_of_charge: str
    shift_state: str | None

    timestamp_format: str
    elevation_unit: str
    odometer_unit: str
    speed_unit: str


class Vehicle(BaseModel):
    class Config:
        orm_mode = True

    id: UUID4
