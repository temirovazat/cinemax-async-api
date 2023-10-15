from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends, Query

from db.elastic import get_elastic
from db.redis import get_redis


class Paginator:
    """Class for retrieving a page request."""

    def __init__(
        self,
        page_number: int = Query(default=1, alias='page[number]', description='Page number', ge=1),
        page_size: int = Query(default=50, alias='page[size]', description='Page size', ge=1, le=100),
    ):
        """
        When initializing the class, it accepts the page number and its size as parameters in the request.

        Args:
            page_number: Page number
            page_size: Page size
        """
        self.page = page_number
        self.size = page_size


class Database:
    """Class with dependencies for working with Elasticsearch and Redis databases."""

    def __init__(
        self,
        elastic: AsyncElasticsearch = Depends(get_elastic),
        redis: Redis = Depends(get_redis),
    ):
        """
        When initializing the class, it injects dependencies for connections to Elasticsearch and Redis.

        Args:
            elastic: Connection to Elasticsearch for data storage
            redis: Connection to Redis for data caching
        """
        self.redis = redis
        self.elastic = elastic
