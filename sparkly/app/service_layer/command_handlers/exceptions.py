from sparkly.app.seedwork.domain import exceptions


class VehicleAlreadyExists(exceptions.DomainValidationError):
    def __init__(self, vehicle_id: str) -> None:
        super().__init__("Vehicle already exists.")
        self.vehicle_id = vehicle_id
