from fastapi import APIRouter
from pydantic import UUID4, BaseModel

from sparkly.app.adapters.db.postgres.session import SESSION_FACTORY
from sparkly.app.domain import commands, queries
from sparkly.app.seedwork.service_layer import message_buses
from sparkly.app.service_layer import command_handlers, query_handlers, uow

router = APIRouter(prefix="/vehicle_data")

UNIT_OF_WORK = uow.VehicleUnitOfWork(session_factory=SESSION_FACTORY)
COMMAND_BUS = message_buses.CommandBus(
    handlers={commands.AddVehicleLog: command_handlers.AddVehicleLog(uow=UNIT_OF_WORK)}
)
QUERY_BUS = message_buses.QueryBus(handlers={queries.GetVehicleLogs: query_handlers.GetVehicleLogs(uow=UNIT_OF_WORK)})


@router.get("/{vehicle_id}")
async def get_vehicle_logs(vehicle_id: UUID4):
    result = await QUERY_BUS.handle(message=queries.GetVehicleLogs(vehicle_id=vehicle_id, limit=10))
    return {"data": result.result}


class AddLogRequest(BaseModel):
    timestamp: str
    speed: int | None
    odometer: float
    state_of_charge: int
    elevation: int
    shift_state: str | None


@router.post("/{vehicle_id}")
async def create_vehicle_log(vehicle_id: UUID4, log: AddLogRequest):
    await COMMAND_BUS.handle(
        message=commands.AddVehicleLog(vehicle_id=vehicle_id, log=commands.VehicleLog(**log.dict()))
    )
    return None
