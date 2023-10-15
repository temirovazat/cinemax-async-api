import time
from functools import wraps
from typing import Callable, List, Union

from elasticsearch import Elasticsearch, helpers, RequestError
from redis import Redis

from settings import Document, logging, MAX_TIME_CONNECTION, Schema, TEST_CONFIG
from testdata.factory import ElasticDocsFactory


def ping(client: Union[Elasticsearch, Redis]) -> Union[Elasticsearch, Redis]:
    """
    Check the connection to the database.

    Args:
        client: Database client

    Raises:
        ConnectionError: If there is no response, raise a connection error

    Returns:
        Elasticsearch | Redis: Client with a connection
    """
    if not client.ping():
        raise ConnectionError('No connection to the database.')
    return client


def connecting(max_time: int, message: str, start_sleep_time=1, factor=2) -> Callable:
    """
    Connect a client to the database and handle failed connections.

    Args:
        max_time (int): Time in seconds allocated for connection attempts.
        message (str): Error message if a connection cannot be established.
        start_sleep_time (int, optional): Initial retry time. Defaults to 1.
        factor (int, optional): How much to increase the wait time by. Defaults to 2.

    Returns:
        Callable: The decorated function.
    """
    def decorator(func) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Union[Elasticsearch, Redis]:  # type: ignore[return]
            delay = start_sleep_time
            while True:
                try:
                    pong = ping(client=func(*args, **kwargs))
                except ConnectionError:
                    if delay > max_time:
                        logging.error(message)
                        break
                    delay *= factor
                    time.sleep(delay)
                else:
                    return pong
        return wrapper
    return decorator


@connecting(max_time=MAX_TIME_CONNECTION, message='Failed to connect to Elasticsearch.')
def get_elastic(host: str, port: int) -> Elasticsearch:
    """
    Get an object for working with the Elasticsearch store.

    Args:
        host: Host
        port: Port

    Returns:
        Elasticsearch: Elasticsearch database client
    """
    return Elasticsearch(f'{host}:{port}', validate_cert=False, use_ssl=False)

@connecting(max_time=MAX_TIME_CONNECTION, message='Failed to connect to Redis.')
def get_redis(host: str, port: int) -> Redis:
    """
    Get an object for working with the Redis cache.

    Args:
        host: Host
        port: Port

    Returns:
        Redis: Redis database client
    """
    return Redis(host=host, port=port)


def create_indices(elastic: Elasticsearch, schemas: List[Schema]):
    """
    Create indices in Elasticsearch.

    Args:
        elastic: Elasticsearch client for executing queries.
        schemas: List of index schemas.
    """
    for schema in schemas:
        try:
            elastic.indices.create(
                index=schema._index._name,
                body=schema._index.to_dict(),
            )
        except RequestError as exc:
            logging.error(exc)
        else:
            logging.info(f'Index {schema._index._name} created.')


def load_data(elastic: Elasticsearch, docs: List[Document]):
    """
    Load data into Elasticsearch.

    Args:
        elastic: Client for executing Elasticsearch queries
        docs: Data to load
    """
    helpers.bulk(
        client=elastic,
        actions=(doc.to_dict() for doc in docs),
        refresh=True,
    )
    logging.info('Data loaded.')


def clear_cache(redis: Redis):
    """
    Clear data cache in Redis.

    Args:
        redis: Client for executing Redis queries
    """
    redis.flushall()
    logging.info('Cache cleared.')


def main():
    """Perform the main program logic."""
    with get_elastic(**TEST_CONFIG.elastic.dict()) as elastic:
        with get_redis(**TEST_CONFIG.redis.dict()) as redis:
            factory = ElasticDocsFactory()
            create_indices(elastic, factory.SCHEMAS)
            load_data(elastic, factory.gendata())
            clear_cache(redis)


if __name__ == '__main__':
    main()
