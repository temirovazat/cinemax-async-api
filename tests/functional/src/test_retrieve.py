import http
from typing import Callable

import pytest


@pytest.mark.parametrize(
    'path, index, check_field',
    [
        ('/films/{id}', 'movies', 'title'),
        ('/persons/{id}', 'persons', 'full_name'),
        ('/genres/{id}', 'genres', 'name'),
    ],
)
@pytest.mark.asyncio
async def test_get_by_id(
    path: str, index: str, check_field: str,  # arguments
    extract_data: Callable, make_get_request: Callable, check_cache: Callable,  # fixtures
):
    """
    Test fetching data by ID.

    Args:
        path: URL resource path
        index: Elasticsearch index name
        check_field: Field of the object to check the data
        extract_data: Fixture for extracting data from the database
        make_get_request: Fixture for making an HTTP request
        check_cache: Fixture for checking data cache
    """
    expected = await extract_data(index)

    response = await make_get_request(path.format(id=expected['id']))
    cache = await check_cache(index, id=expected['id'])

    assert response.status == http.HTTPStatus.OK
    assert response.body[check_field] == expected[check_field]
    assert cache
