from dependency_injector import containers, providers

from sparkly.app.domain import commands, queries
from sparkly.app.seedwork.service_layer import CommandBus, QueryBus
from sparkly.app.service_layer import command_handlers, query_handlers


class MessageBusContainer(containers.DeclarativeContainer):
    unit_of_work = providers.DependenciesContainer()
    command = providers.Factory(
        CommandBus,
        handlers=providers.Dict(
            {
                commands.AddVehicle: providers.Factory(command_handlers.AddVehicle, uow=unit_of_work.vehicle),
                commands.AddVehicleLog: providers.Factory(command_handlers.AddVehicleLog, uow=unit_of_work.vehicle),
            }
        ),
    )
    query = providers.Factory(
        QueryBus,
        handlers=providers.Dict(
            {
                queries.GetVehicleLogs: providers.Factory(query_handlers.GetVehicleLogs, uow=unit_of_work.vehicle),
            }
        ),
    )
