import pytest
from fastapi import FastAPI
from fastapi import status
from httpx import AsyncClient

from tests.conftest import TestCommandBus

pytestmark = pytest.mark.asyncio


class TestCreateVehicle:
    async def test_create_new_vehicle(
        self,
        app: FastAPI,
        test_client: AsyncClient,
        command_bus: TestCommandBus,
    ) -> None:
        res = await test_client.post(
            app.url_path_for("vehicles:create-vehicle"),
            json={"vehicle_id": "03103e56-ba9b-4c79-830a-4018e2f4962c"},
        )

        assert res.status_code == status.HTTP_201_CREATED
        assert res.json() == {}

    async def test_create_duplicated_vehicle(
        self,
        app: FastAPI,
        test_client: AsyncClient,
        command_bus: TestCommandBus,
    ) -> None:
        res = await test_client.post(
            app.url_path_for("vehicles:create-vehicle"),
            json={"vehicle_id": "03103e56-ba9b-4c79-830a-4018e2f4962c"},
        )

        assert res.status_code == status.HTTP_201_CREATED
        assert res.json() == {}

        res = await test_client.post(
            app.url_path_for("vehicles:create-vehicle"),
            json={"vehicle_id": "03103e56-ba9b-4c79-830a-4018e2f4962c"},
        )

        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert res.json() == {}
