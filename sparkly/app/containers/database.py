import json
from typing import Any

from dependency_injector import containers
from dependency_injector import providers
from pydantic.json import pydantic_encoder
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from sparkly.app.config import settings


def get_engine() -> AsyncEngine:
    def json_serializer(*args: Any, **kwargs: Any) -> str:
        return json.dumps(*args, default=pydantic_encoder, **kwargs)

    return create_async_engine(
        url=settings.db.get_async_uri().get_secret_value(),
        pool_pre_ping=True,
        echo=settings.db.ECHO_LOGS,
        json_serializer=json_serializer,
    )


def get_session(engine: AsyncEngine) -> sessionmaker:
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )


class PostgresContainer(containers.DeclarativeContainer):
    engine = providers.Singleton(get_engine)
    session_factory = providers.Singleton(get_session, engine=engine)
