from pydantic import UUID4, Field

from sparkly.app.seedwork import domain


class GetVehicleLogs(domain.Query):
    vehicle_id: UUID4
    limit: int = Field(default=10, le=1000, ge=1)


class ListVehicles(domain.Query):
    limit: int = Field(default=10, le=1000, ge=1)
