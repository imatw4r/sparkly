import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient

from sparkly.app.entrypoints.http.fastapi.main import app as api


@pytest.fixture(scope="session")
def app() -> FastAPI:
    return api


@pytest.fixture(scope="session")
def test_client(app: FastAPI) -> AsyncClient:
    return AsyncClient(app=app)
