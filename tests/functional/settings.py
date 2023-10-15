import logging
from typing import Optional, Type, Union

from pydantic import BaseModel, BaseSettings, Field, validator

from testdata.schemas.genre import Genre
from testdata.schemas.movie import Movie
from testdata.schemas.person import Person

Schema = Type[Union[Movie, Person, Genre]]
Document = Union[Movie, Person, Genre]

logging.basicConfig(level=logging.INFO)


class TestDBConfig(BaseModel):
    """Class for validating connection settings to the test database."""

    host: str
    port: int


class RedisConfig(TestDBConfig):
    """Class with settings for connecting to Redis."""


class ElasticConfig(TestDBConfig):
    """Class with settings for connecting to Elasticsearch."""


class UrlPath(BaseModel):
    """Class for providing the URL of the service."""

    protocol: str = Field(default='http://')
    domain: str = Field(default='127.0.0.1')
    port: int = Field(default=8000)
    api_path: str = Field(default='/api/v1')

    @validator('port')
    def get_port(cls, port: int) -> str:
        """
        Transform the port for proper URL representation.

        Args:
            port: The port to connect to the service.

        Returns:
            str: The port as part of the URL.
        """
        return f':{port}' if port not in {80, 443} else ''

    def __str__(self) -> str:
        """Return the service URL as a string.

        Returns:
            str: The URL of the service.
        """
        return ''.join(value for _, value in self.__repr_args__())

    class Config:
        """Validation settings."""

        validate_all = True


class QueryParams(BaseModel):
    """Class for providing query parameters in the URL."""

    filter: Optional[str] = Field(alias='filter[genre]')
    page_number: Optional[int] = Field(default=1, alias='page[number]')
    page_size: Optional[int] = Field(default=50, alias='page[size]')
    query: Optional[str]
    sort: Optional[str]

    class Config:
        """Validation settings."""

        allow_population_by_field_name = True


class TestMainSettings(BaseSettings):
    """Class with settings for testing the project."""

    secret_key: str = Field(default='secret_key')
    url: UrlPath = Field(default_factory=UrlPath)
    elastic: TestDBConfig = Field(default=ElasticConfig(host='127.0.0.1', port=9200))
    redis: TestDBConfig = Field(default=RedisConfig(host='127.0.0.1', port=6379))


TEST_CONFIG = TestMainSettings(_env_file='.env', _env_nested_delimiter='_')
MAX_PAGE_SIZE = 100
MAX_TIME_CONNECTION = 15
