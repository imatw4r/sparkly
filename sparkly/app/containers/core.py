from logging.config import dictConfig

from dependency_injector import containers
from dependency_injector import providers

from sparkly.app.adapters.db import sqlalchemy as sqlalchemy_orm
from sparkly.app.config import settings


class CoreContainer(containers.DeclarativeContainer):
    logging: providers.Resource = providers.Resource(dictConfig, config=settings.logger.get_config())
    orm_mapper: providers.Resource = providers.Resource(sqlalchemy_orm.mappers)
