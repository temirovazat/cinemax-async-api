from typing import AsyncGenerator, Callable, Optional
from uuid import UUID

import aioredis
import pytest
import pytest_asyncio

from settings import TEST_CONFIG, QueryParams


@pytest_asyncio.fixture(scope='session')
async def redis() -> AsyncGenerator[aioredis.Redis, None]:
    """
    Fixture for connecting to Redis and clearing data cache after tests.

    Yields:
        aioredis.Redis: Object for asynchronous Redis interaction
    """
    redis = await aioredis.create_redis_pool(
        tuple(TEST_CONFIG.redis.dict().values()), minsize=10, maxsize=20,
    )
    try:
        yield redis
    finally:
        await redis.flushall()
        redis.close()
        await redis.wait_closed()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def clear_cache(redis: aioredis.Redis):
    """
    Fixture for clearing the cache before running tests.

    Args:
        redis: Redis client fixture
    """
    await redis.flushall()


def get_redis_key(index: str, id: Optional[UUID], **kwargs) -> str:
    """
    Get the key for data in the Redis cache.

    Args:
        index: Elasticsearch index name
        id: Data ID
        kwargs: Named parameters in the URL query

    Returns:
        str: Key for data in Redis
    """
    params = [
        f'{field}::{value}' for field, value in QueryParams(**kwargs).dict().items()
    ]
    if id:
        return '{index}::id::{id}'.format(index=index, id=id)
    return '{index}::{params}'.format(index=index, params='::'.join(params))


@pytest.fixture(scope='session')
def check_cache(redis: aioredis.Redis) -> Callable:
    """
    Fixture with a nested function for retrieving data from the cache.

    Args:
        redis: Redis client fixture

    Returns:
        Callable: Fixture function to retrieve data from Redis cache
    """
    async def inner(index: str, id: Optional[UUID] = None, **kwargs) -> bytes:
        cache = await redis.get(
            key=get_redis_key(index=index, id=id, **kwargs),
        )
        return cache
    return inner
