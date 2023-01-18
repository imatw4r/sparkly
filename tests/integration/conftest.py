import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from sparkly.app.entrypoints.http.fastapi.main import app as api
from sparkly.app.seedwork import domain, service_layer


class TestCommandBus(service_layer.CommandBus):
    def __init__(self) -> None:
        self.commands: list[domain.Command] = []

    async def handle(self, message: domain.Command) -> service_layer.HandlerResult:
        self.commands.append(message)
        return service_layer.HandlerResult(result=None)


@pytest.fixture(scope="session")
def app() -> FastAPI:
    return api


@pytest.fixture(scope="session")
def test_client(app: FastAPI) -> AsyncClient:
    return AsyncClient(app=app, base_url="http://sparkly")


@pytest.fixture()
def command_bus() -> service_layer.CommandBus:
    return TestCommandBus()
