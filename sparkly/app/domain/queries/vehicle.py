from pydantic import UUID4

from sparkly.app.seedwork import domain


class GetVehicleLogs(domain.Query):
    vehicle_id: UUID4


class ListVehicles(domain.Query):
    pass
