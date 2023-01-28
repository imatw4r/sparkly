from typing import Generic
from typing import TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pydantic import parse_obj_as
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON
from sqlalchemy.types import TypeDecorator

T_pydantic = TypeVar("T_pydantic", bound=BaseModel)


class PydanticType(TypeDecorator, Generic[T_pydantic]):
    impl = JSON
    cache_ok = True

    def __init__(self, pydantic_class: type[T_pydantic]) -> None:
        super().__init__()
        self.pydantic_class = pydantic_class

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(JSONB())
        raise ValueError("Field only support 'postgresql' dialect.")

    def process_bind_param(self, value, dialect):
        encoded_value = None
        if value:
            encoded_value = jsonable_encoder(obj=value)
        return encoded_value

    def process_result_value(self, value, dialect):
        parsed_obj = None
        if value:
            parsed_obj = parse_obj_as(self.pydantic_class, value)
        return parsed_obj
