from dependency_injector import containers
from dependency_injector import providers

from sparkly.app.domain import commands
from sparkly.app.domain import queries
from sparkly.app.seedwork.service_layer import CommandBus
from sparkly.app.seedwork.service_layer import QueryBus
from sparkly.app.service_layer import command_handlers
from sparkly.app.service_layer import query_handlers


class MessageBusContainer(containers.DeclarativeContainer):
    unit_of_work = providers.DependenciesContainer()
    command = providers.Factory(
        CommandBus,
        handlers=providers.Dict(
            {
                commands.AddVehicle: providers.Factory(command_handlers.AddVehicle, uow=unit_of_work.vehicle),
                commands.AddVehicleLog: providers.Factory(command_handlers.AddVehicleLog, uow=unit_of_work.vehicle),
            },
        ),
    )
    query = providers.Factory(
        QueryBus,
        handlers=providers.Dict(
            {
                queries.GetVehicleLogs: providers.Factory(query_handlers.GetVehicleLogs, uow=unit_of_work.vehicle),
                queries.ListVehicles: providers.Factory(query_handlers.ListVehicles, uow=unit_of_work.vehicle),
            },
        ),
    )
