import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from .base import metadata

vehicle = sa.Table(
    "vehicle",
    metadata,
    sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
)

vehicle_logs = sa.Table(
    "vehicle_logs",
    metadata,
    sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
    sa.Column(
        "vehicle_id",
        sa.ForeignKey(vehicle.c.id, name="vehicle_logs_vehicle_id_fk"),
    ),
    sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
    sa.Column("odometer", sa.Integer(), nullable=False),
    sa.Column("odometer_unit", sa.String(10), nullable=False),
    sa.Column("elevation", sa.Integer(), nullable=False),
    sa.Column("elevation_unit", sa.String(10), nullable=False),
    sa.Column("state_of_change", sa.Integer(), nullable=False),
    sa.Column("shift_state", sa.String(1), nullable=True),
    sa.Column("speed", sa.Integer(), nullable=True),
    sa.Column("speed_unit", sa.String(10), nullable=True),
    sa.Column("created_at", sa.DateTime, default=datetime.utcnow),
)

vehicle_to_logs = sa.Table(
    "vehicle_to_logs",
    metadata,
    sa.Column(
        "vehicle_id",
        sa.ForeignKey("vehicle.id", name="vehicle_to_logs_vehicle_id_fk"),
    ),
    sa.Column(
        "log_id",
        sa.ForeignKey("vehicle_logs.id", name="vehicle_to_logs_vehicle_logs_id_fk"),
    ),
)
