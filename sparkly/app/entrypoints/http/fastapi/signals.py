from fastapi import FastAPI

from sparkly.app.adapters.db.postgres import session


async def dispose_sqlalchemy_engine_signal() -> None:
    await session.ENGINE.dispose()


def setup_signals(app: FastAPI) -> None:
    app.add_event_handler(event_type="shutdown", func=dispose_sqlalchemy_engine_signal)
