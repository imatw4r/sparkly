from dependency_injector import containers
from dependency_injector import providers

from sparkly.app.service_layer.uow import VehicleUnitOfWork


class UnitOfWorkContainer(containers.DeclarativeContainer):
    database = providers.DependenciesContainer()
    vehicle = providers.Factory(VehicleUnitOfWork, session_factory=database.session_factory)
