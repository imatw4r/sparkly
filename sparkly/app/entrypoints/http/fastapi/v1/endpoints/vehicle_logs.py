from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page, add_pagination, paginate
from pydantic import UUID4, BaseModel

from sparkly.app.containers import SparklyContainer
from sparkly.app.domain import commands, queries
from sparkly.app.seedwork.service_layer import message_buses

router = APIRouter(prefix="/vehicle_data")


@router.get(
    "/{vehicle_id}",
    response_model=Page[dict],
    name="vehicle_logs:get-logs-for-vehicle",
    status_code=status.HTTP_201_CREATED,
)
@inject
async def get_vehicle_logs(
    vehicle_id: UUID4, query_bus: message_buses.QueryBus = Depends(Provide[SparklyContainer.message_busses.query])
):
    result = await query_bus.handle(message=queries.GetVehicleLogs(vehicle_id=vehicle_id, limit=10))
    return paginate([log.as_dict() for log in result.result])


class CreateVehicleLogRequest(BaseModel):
    timestamp: str
    speed: int | None
    odometer: float
    state_of_charge: int
    elevation: int
    shift_state: str | None


@router.post("/{vehicle_id}", name="vehicle_logs:create-log-for-vehicle", status_code=status.HTTP_201_CREATED)
@inject
async def create_vehicle_log(
    vehicle_id: UUID4,
    log: CreateVehicleLogRequest,
    query_bus: message_buses.CommandBus = Depends(Provide[SparklyContainer.message_busses.query]),
):
    await query_bus.handle(
        message=commands.AddVehicleLog(vehicle_id=vehicle_id, log=commands.VehicleLog(**log.dict()))
    )
    return None


add_pagination(router)
