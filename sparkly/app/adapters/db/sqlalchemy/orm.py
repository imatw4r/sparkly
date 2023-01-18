import uuid

from sqlalchemy import DECIMAL, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry, relationship

from sparkly.app.domain import entities, value_objects

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
    Column("timestamp", DateTime(timezone=True), nullable=False),
    Column("timestamp_format", String(length=40), nullable=False, server_default="ISO8601"),
    Column("speed", Integer()),
    Column("speed_unit", String(length=20)),
    Column("odometer", DECIMAL(precision=10, scale=2), nullable=False),
    Column("odometer_unit", String(length=20), nullable=False),
    Column("state_of_charge", Integer(), nullable=False),
    Column("elevation", Integer(), nullable=False),
    Column("elevation_unit", String(length=20), nullable=False),
    Column("shift_state", String(length=1)),
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


def mappers() -> None:
    """
    Function responsible for mapping Domain objects into SQLAlchemy objects.
    Executing this function allows us to execute normal SQLAlchemy
    selects, inserts, etc on actual Domain objects.
    """
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
