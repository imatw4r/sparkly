from fastapi import FastAPI

from sparkly.app.entrypoints.http.fastapi.middlewares import setup_middlewares
from sparkly.app.entrypoints.http.fastapi.signals import setup_signals
from sparkly.app.entrypoints.http.fastapi.v1.api import router as api_v1

app = FastAPI()
app.include_router(api_v1)

setup_signals(app=app)
setup_middlewares(app=app)
