from typing import Generic

from . import uow


class SQLAlchemyUnitOfWorkMixin(Generic[uow.T_sqlalchemy_uow]):
    def __init__(self, uow: uow.T_sqlalchemy_uow) -> None:
        self.uow = uow
