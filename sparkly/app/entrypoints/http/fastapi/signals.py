from dependency_injector.wiring import Provide, inject
from fastapi import FastAPI

from sparkly.app.containers import SparklyContainer
from sqlalchemy.ext.asyncio import AsyncEngine


@inject
async def dispose_sqlalchemy_engine_signal(engine: AsyncEngine = Provide[SparklyContainer.database.engine]) -> None:
    await engine.dispose()


def setup_signals(app: FastAPI) -> None:
    app.add_event_handler(event_type="shutdown", func=dispose_sqlalchemy_engine_signal)
