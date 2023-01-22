from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_pagination import Page, add_pagination
from pydantic import UUID4, BaseModel

from sparkly.app.containers import SparklyContainer
from sparkly.app.domain import commands, queries
from sparkly.app.entrypoints.http.fastapi import models
from sparkly.app.seedwork.service_layer import message_buses
from sparkly.app.service_layer.command_handlers import VehicleAlreadyExists

router = APIRouter(prefix="/vehicle")


class CreateVehicleRequest(BaseModel):
    vehicle_id: UUID4


@router.post("/", name="vehicles:create-vehicle", status_code=status.HTTP_201_CREATED)
@inject
async def create_vehicle(
    request: CreateVehicleRequest,
    command_bus: message_buses.CommandBus = Depends(Provide[SparklyContainer.message_busses.command]),
):
    try:
        await command_bus.handle(message=commands.AddVehicle(vehicle_id=request.vehicle_id))
    except VehicleAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return None


@router.get("/", response_model=Page[models.Vehicle], name="vehicle:list-vehicles")
@inject
async def list_vehicles(
    command_bus: message_buses.QueryBus = Depends(Provide[SparklyContainer.message_busses.query]),
):
    result = await command_bus.handle(message=queries.ListVehicles())
    return await result.result


add_pagination(router)
