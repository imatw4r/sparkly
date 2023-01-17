from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import UUID4, BaseModel

from sparkly.app.containers import SparklyContainer
from sparkly.app.domain import commands, queries
from sparkly.app.seedwork.service_layer import message_buses

router = APIRouter(prefix="/vehicle_data")


@router.get("/{vehicle_id}")
@inject
async def get_vehicle_logs(
    vehicle_id: UUID4, query_bus: message_buses.QueryBus = Depends(Provide[SparklyContainer.message_busses.query])
):
    result = await query_bus.handle(message=queries.GetVehicleLogs(vehicle_id=vehicle_id, limit=10))
    return {"count": len(result.result), "data": result.result}


class CreateVehicleRequest(BaseModel):
    vehicle_id: UUID4


@router.post("/")
@inject
async def create_vehicle(
    request: CreateVehicleRequest,
    command_bus: message_buses.CommandBus = Depends(Provide[SparklyContainer.message_busses.command]),
):
    await command_bus.handle(message=commands.AddVehicle(vehicle_id=request.vehicle_id))
    return None


class CreateVehicleLogRequest(BaseModel):
    timestamp: str
    speed: int | None
    odometer: float
    state_of_charge: int
    elevation: int
    shift_state: str | None


@router.post("/{vehicle_id}")
@inject
async def create_vehicle_log(
    vehicle_id: UUID4,
    log: CreateVehicleLogRequest,
    command_bus: message_buses.CommandBus = Depends(Provide[SparklyContainer.message_busses.command]),
):
    await command_bus.handle(
        message=commands.AddVehicleLog(vehicle_id=vehicle_id, log=commands.VehicleLog(**log.dict()))
    )
    return None
