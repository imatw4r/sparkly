import pytest
from fastapi import FastAPI
from fastapi import status
from httpx import AsyncClient
from pydantic import UUID4

from sparkly.app.domain import commands
from tests.conftest import TestCommandBus

pytestmark = pytest.mark.asyncio


class TestCreateVehicle:
    async def test_create_vehicle(self, app: FastAPI, test_client: AsyncClient, command_bus: TestCommandBus) -> None:
        with app.container.message_busses.command.override(command_bus):  # type: ignore[attr-defined]
            res = await test_client.post(
                app.url_path_for("vehicles:create-vehicle"),
                json={"vehicle_id": "03103e56-ba9b-4c79-830a-4018e2f4962c"},
            )

            assert res.status_code == status.HTTP_201_CREATED
            assert command_bus.commands[0] == commands.AddVehicle(
                vehicle_id=UUID4("03103e56-ba9b-4c79-830a-4018e2f4962c"),
            )
