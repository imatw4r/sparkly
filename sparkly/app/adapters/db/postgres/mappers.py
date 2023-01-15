from sqlalchemy.orm import mapper, relationship

from sparkly.app.domain.entities import Vehicle
from sparkly.app.domain.value_objects.vehicle import VehicleLog

from .models import vehicle, vehicle_logs, vehicle_to_logs


def start_mappers():
    vehicle_log_mapper = mapper(VehicleLog, vehicle_logs)
    mapper(
        Vehicle,
        vehicle,
        properties={
            "logs": relationship(
                vehicle_log_mapper, order_by=lambda: vehicle_log_mapper.timestamp, secondary=vehicle_to_logs
            )
        },
    )
