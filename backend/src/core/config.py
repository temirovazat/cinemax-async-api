from functools import lru_cache
from typing import ClassVar, Union

from pydantic import BaseSettings, Field

from models.film import Film, FilmList, FilmModified
from models.genre import Genre, GenreList
from models.person import Person, PersonList

CinemaObject = Union[Film, FilmModified, Person, Genre]
CinemaObjectList = Union[FilmList, PersonList, GenreList]


class RedisConfig(BaseSettings):
    """Class with Redis connection settings."""

    host: str = '127.0.0.1'
    port: int = 6379


class ElasticConfig(BaseSettings):
    """Class with Elasticsearch connection settings."""

    host: str = '127.0.0.1'
    port: int = 9200


class LogstashConfig(BaseSettings):
    """Class with Logstash connection settings."""

    host: str = 'localhost'
    port: int = 5044


class FastApiConfig(BaseSettings):
    """Class with FastAPI connection settings."""

    host: str = '0.0.0.0'
    port: int = 8000
    debug: bool = False
    docs: str = 'openapi'
    secret_key: str = 'secret_key'
    project_name: str = 'Read-only API for an online cinema'
    cache_expire_in_seconds: ClassVar[int] = 60


class MainSettings(BaseSettings):
    """Class with main project settings."""

    fastapi: FastApiConfig = Field(default_factory=FastApiConfig)
    elastic: ElasticConfig = Field(default_factory=ElasticConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    logstash: LogstashConfig = Field(default_factory=LogstashConfig)


@lru_cache()
def get_settings() -> MainSettings:
    """
    Create a settings object as a singleton.

    Returns:
        MainSettings: Settings object
    """
    return MainSettings(_env_file='.env', _env_nested_delimiter='_')


CONFIG = get_settings()
