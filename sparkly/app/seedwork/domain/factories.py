from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ValidationError

from .entities import Entity
from .exceptions import DomainValidationError
from .value_objects import ValueObject

T_factory_attrs = TypeVar("T_factory_attrs", bound=BaseModel)
T_domain_object = TypeVar("T_domain_object", bound=ValueObject | Entity)


class DomainFactory(Generic[T_factory_attrs, T_domain_object]):
    domain_class: type[T_domain_object]

    @classmethod
    def convert_attrs(cls, attrs: T_factory_attrs) -> dict[str, Any]:
        return attrs.dict()

    @classmethod
    def create_from(cls, attrs: T_factory_attrs) -> T_domain_object:
        try:
            converted_attrs = cls.convert_attrs(attrs=attrs)
            return cls.domain_class(**converted_attrs)
        except ValidationError as pydantic_error:
            raise DomainValidationError(pydantic_error) from None
