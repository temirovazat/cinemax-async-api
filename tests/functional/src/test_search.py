from typing import Callable

import pytest


@pytest.mark.parametrize(
    'path, index, search_field',
    [
        ('/films/search', 'movies', 'title'),
        ('/persons/search', 'persons', 'full_name'),
    ],
)
@pytest.mark.asyncio
async def test_get_search(
    path: str, index: str, search_field: str,  # args
    extract_data: Callable, make_get_request: Callable, check_cache: Callable,  # fixtures
):
    """
    Test full-text search.

    Args:
        path: Path to the URL resource
        index: Name of the Elasticsearch index
        search_field: The field of the object to search by
        extract_data: Fixture that extracts data from the database
        make_get_request: Fixture that performs an HTTP request
        check_cache: Fixture that checks data cache
    """
    expected = await extract_data(index)

    response = await make_get_request(path, query=expected[search_field])
    cache = await check_cache(index, query=expected[search_field])

    assert expected[search_field] in {data[search_field] for data in response.body}
    assert cache
