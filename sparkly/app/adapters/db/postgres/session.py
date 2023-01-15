from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from sparkly.config import settings

ENGINE = create_async_engine(url=settings.db.get_async_uri().get_secret_value(), pool_pre_ping=True)
SESSION_FACTORY = sessionmaker(ENGINE, expire_on_commit=False, autocommit=False, autoflush=False, class_=AsyncSession)
