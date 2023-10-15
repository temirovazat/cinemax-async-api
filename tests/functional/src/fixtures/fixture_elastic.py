import random
from typing import AsyncGenerator, Callable, Dict, List, Optional
from uuid import UUID

import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch

from settings import TEST_CONFIG


@pytest_asyncio.fixture(scope='session')
async def elastic() -> AsyncGenerator[AsyncElasticsearch, None]:
    """
    Fixture for connecting to Elasticsearch and clearing the database data after tests.

    Yields:
        AsyncElasticsearch: Object for asynchronous work with Elasticsearch
    """
    elastic = AsyncElasticsearch(
        hosts='{host}:{port}'.format(**TEST_CONFIG.elastic.dict()),
    )
    try:
        yield elastic
    finally:
        await elastic.indices.delete('_all')
        await elastic.close()


def get_random_doc(data: List[Dict]) -> Dict:
    """
    Get a random element from the list.

    Args:
        data: List of documents from Elasticsearch

    Returns:
        dict: A random document
    """
    docs = [doc['_source'] for doc in data['hits']['hits']]  # type: ignore[call-overload]
    return docs[random.randrange(len(docs))] if docs else {}


@pytest.fixture(scope='session')
def extract_data(elastic: AsyncElasticsearch) -> Callable:
    """
    Fixture with a nested function for retrieving data from the database.

    Args:
        elastic: Elasticsearch client fixture

    Returns:
        Callable: Fixture function to retrieve data from the Elasticsearch database
    """
    async def inner(index: str, id: Optional[UUID] = None) -> dict:
        if not id:
            data = await elastic.search(index=index, size=1000)
            return get_random_doc(data)
        return await elastic.get_source(index=index, id=id)
    return inner
