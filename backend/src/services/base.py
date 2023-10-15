import abc
from enum import Enum
from functools import wraps
from typing import Callable, Type, Union

from pydantic import BaseModel, parse_obj_as, parse_raw_as

from core.config import CinemaObject, CinemaObjectList
from db.elastic import ElasticStorage
from db.redis import RedisStorage


class ElasticIndices(Enum):
    """Indices with cinema data in Elasticsearch."""

    movies = 'movies'
    persons = 'persons'
    genres = 'genres'


class BaseService(ElasticStorage, RedisStorage, abc.ABC):
    """Abstract service class for implementing cinema-related business logic."""

    index: ElasticIndices
    model: Type[Union[CinemaObject, CinemaObjectList]]

    @property
    @abc.abstractmethod
    def redis_key(self) -> str:
        """Key for Redis cache data as a string."""

    @abc.abstractmethod
    async def get(self) -> Union[CinemaObject, CinemaObjectList]:
        """Retrieve a representation of cinema data."""

    class Config:
        """Validation settings."""

        use_enum_values = True


def redis_cache(expire: int) -> Callable:
    """
    Decorate to fetch and cache cinema data in the Redis cache.

    Args:
        expire (int): Cache expiration time

    Returns:
        Callable: Decorated function that retrieves a representation of cinema data.
    """
    def decorator(get) -> Callable:
        @wraps(get)
        async def wrapper(*args, **kwargs) -> BaseModel:
            self: BaseService = args[0]
            data = await self.get_redis_value(self.redis_key)
            if not data:
                data = parse_obj_as(
                    self.model, obj=await get(*args, **kwargs),
                ).json()
                await self.set_redis_value(self.redis_key, data, expire=expire)
            return parse_raw_as(self.model, b=data)
        return wrapper
    return decorator
