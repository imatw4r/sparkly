from fastapi import FastAPI

from sparkly.app.containers import init_main_container
from sparkly.app.entrypoints.http.fastapi.middlewares import setup_middlewares
from sparkly.app.entrypoints.http.fastapi.signals import setup_signals
from sparkly.app.entrypoints.http.fastapi.v1.api import router as api_v1


def create_app() -> FastAPI:
    container = init_main_container(
        modules=[
            "sparkly.app.entrypoints.http.fastapi.signals",
            "sparkly.app.entrypoints.http.fastapi.v1.endpoints.vehicle",
            "sparkly.app.entrypoints.http.fastapi.v1.endpoints.vehicle_logs",
        ]
    )

    app = FastAPI()
    app.container = container  # type: ignore
    app.include_router(api_v1)

    setup_signals(app=app)
    setup_middlewares(app=app)
    return app


app = create_app()
