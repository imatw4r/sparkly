from easy_profile import SessionProfiler
from easy_profile import StreamReporter
from fastapi import FastAPI
from fastapi import Request
from fastapi import Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint

from sparkly.app.config import settings


class ProfilerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        profiler = SessionProfiler()
        reporter = StreamReporter()
        profiler.begin()
        response = await call_next(request)
        profiler.commit()
        reporter.report(stats=profiler.stats, path=request.url.path)
        return response


def setup_middlewares(app: FastAPI) -> None:
    if settings.db.ENABLE_PROFILER:
        app.add_middleware(middleware_class=ProfilerMiddleware)
