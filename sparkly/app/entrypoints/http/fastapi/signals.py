from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine

from sparkly.app.containers import SparklyContainer


@inject
async def dispose_sqlalchemy_engine_signal(engine: AsyncEngine = Provide[SparklyContainer.database.engine]) -> None:
    await engine.dispose()


def setup_signals(app: FastAPI) -> None:
    app.add_event_handler(event_type="shutdown", func=dispose_sqlalchemy_engine_signal)
