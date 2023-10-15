from typing import Optional

from aioredis import Redis
from aioredis.errors import ConnectionClosedError

from db.base import DatabaseModel
from core.decorators import backoff

connection: Optional[Redis] = None


async def get_redis() -> Redis:
    """
    Establish a connection to Redis, which is required when implementing dependencies.

    Returns:
        Redis: Redis connection
    """
    return connection


class RedisStorage(DatabaseModel):
    """A class for working with Redis storage in the form of a data cache."""

    redis: Redis

    @backoff(errors=(ConnectionClosedError))
    async def get_redis_value(self, key: str) -> bytes:
        """
        Get data from Redis cache.

        Args:
            key: The key of the data

        Returns:
            bytes: Data from cache
        """
        value = await self.redis.get(key=key)
        return value

    @backoff(errors=(ConnectionClosedError))
    async def set_redis_value(self, key: str, data: str, **kwargs):
        """
        Write data to Redis cache.

        Args:
            key: Data key
            data: Data to write
            kwargs: Optional named arguments
        """
        await self.redis.set(key, data, **kwargs)
