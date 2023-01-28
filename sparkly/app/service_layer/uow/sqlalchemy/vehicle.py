from __future__ import annotations

from sparkly.app.adapters.repos.postgresql.repositories import VehicleRepository
from sparkly.app.seedwork import service_layer


class VehicleUnitOfWork(service_layer.SQLAlchemyUnitOfWork[VehicleRepository]):
    repository_cls = VehicleRepository
