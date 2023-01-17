from fastapi import APIRouter

from .endpoints.vehicle import router as vehicle_data_api

router = APIRouter(prefix="/v1")

router.include_router(vehicle_data_api)
