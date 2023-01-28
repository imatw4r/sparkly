import uuid

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import DECIMAL
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry

from sparkly.app.domain import entities
from sparkly.app.domain import value_objects

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
    Column("vehicle_id", UUID(as_uuid=True), nullable=False),
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


def mappers() -> None:
    """
    Function responsible for mapping Domain objects into SQLAlchemy objects.
    Executing this function allows us to execute normal SQLAlchemy
    selects, inserts, etc on actual Domain objects.
    """
    mapper_registry.map_imperatively(class_=value_objects.VehicleLog, local_table=log_table)
    mapper_registry.map_imperatively(class_=entities.Vehicle, local_table=vehicle_table)
