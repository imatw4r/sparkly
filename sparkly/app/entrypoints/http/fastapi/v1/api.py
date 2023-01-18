from fastapi import APIRouter

from .endpoints.vehicle import router as vehicle_router
from .endpoints.vehicle_logs import router as vehicle_logs_router

router = APIRouter(prefix="/v1")

router.include_router(vehicle_router)
router.include_router(vehicle_logs_router)
