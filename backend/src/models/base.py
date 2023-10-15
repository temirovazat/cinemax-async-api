from typing import Callable
from uuid import UUID

import orjson
from pydantic import BaseModel


def orjson_dumps(value: object, *, default: Callable) -> str:
    """
    Convert data to a JSON string, handling objects based on a Pydantic class.

    Args:
        value: Data to convert.
        default: Function for objects that cannot be serialized.

    Returns:
        str: JSON string.
    """
    return orjson.dumps(value, default=default).decode()


class UUIDMixin(BaseModel):
    """Mixin for storing primary keys."""

    uuid: UUID


class OrjsonMixin(BaseModel):
    """Mixin to replace the standard json handling with a faster one."""

    class Config:
        """Serialization Settings."""

        json_loads = orjson.loads
        json_dumps = orjson_dumps
