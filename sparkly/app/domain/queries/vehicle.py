from pydantic import UUID4, Field

from sparkly.app.seedwork import domain


class GetVehicleLogs(domain.Query):
    vehicle_id: UUID4
    limit: int = Field(default=10, le=1000, ge=1)
