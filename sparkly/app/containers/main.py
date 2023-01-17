from dependency_injector import containers, providers

from .core import CoreContainer
from .database import PostgresContainer
from .message_busses import MessageBusContainer
from .unit_of_work import UnitOfWorkContainer


class SparklyContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration()

    core = providers.Container(CoreContainer)
    database = providers.Container(PostgresContainer)
    unit_of_work = providers.Container(UnitOfWorkContainer, database=database)
    message_busses = providers.Container(MessageBusContainer, unit_of_work=unit_of_work)
