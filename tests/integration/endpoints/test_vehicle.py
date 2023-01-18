import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestCreateVehicle:
    async def test_create_vehicle(self, app: FastAPI, test_client: AsyncClient) -> None:
        res = await test_client.post(
            app.url_path_for("vehicles:create-vehicle"), json={"vehicle_id": "03103e56-ba9b-4c79-830a-4018e2f4962c"}
        )

        assert res.status_code == status.HTTP_201_CREATED
