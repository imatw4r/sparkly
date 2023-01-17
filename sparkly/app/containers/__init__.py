from .core import CoreContainer
from .database import PostgresContainer
from .main import SparklyContainer
from .message_busses import MessageBusContainer
from .unit_of_work import UnitOfWorkContainer


def init_main_container(modules: list[str]) -> SparklyContainer:
    container = SparklyContainer()
    container.core.init_resources()
    container.wire(modules=modules)
    return container
