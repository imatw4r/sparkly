import uuid

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry, relationship

from sparkly.app.domain import entities, value_objects
from sparkly.app.utils.sqlalchemy import PydanticType

mapper_registry = registry()
metadata = mapper_registry.metadata

log_table = Table(
    "log",
    metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
    ),
    Column(
        "timestamp",
        PydanticType(pydantic_class=value_objects.Timestamp),
    ),
    Column("speed", PydanticType(pydantic_class=value_objects.VehicleSpeed)),
    Column(
        "odometer",
        PydanticType(pydantic_class=value_objects.Odometer),
    ),
    Column(
        "state_of_charge",
        PydanticType(pydantic_class=value_objects.StateOfCharge),
    ),
    Column(
        "elevation",
        PydanticType(pydantic_class=value_objects.Elevation),
    ),
    Column("shift_state", PydanticType(pydantic_class=value_objects.ShiftState)),
)

vehicle_table = Table(
    "vehicle",
    metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
    ),
)

vehicle_to_log_table = Table(
    "vehicle_to_log",
    metadata,
    Column(
        "vehicle_id",
        ForeignKey(column="vehicle.id", name="vehicle_to_log__vehicle_id_fk"),
        primary_key=True,
    ),
    Column(
        "log_id",
        ForeignKey(column="log.id", name="vehicle_to_log__log_id_fk"),
        primary_key=True,
    ),
)


def start_mappers():
    vehicle_log_mapper = mapper_registry.map_imperatively(class_=value_objects.VehicleLog, local_table=log_table)
    mapper_registry.map_imperatively(
        class_=entities.Vehicle,
        local_table=vehicle_table,
        properties={
            "logs": relationship(
                vehicle_log_mapper,
                order_by=lambda: vehicle_log_mapper.c.timestamp,
                secondary=vehicle_to_log_table,
                lazy="joined",
            )
        },
    )
