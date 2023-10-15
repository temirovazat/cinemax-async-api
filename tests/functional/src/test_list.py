import http
from typing import Callable

import pytest


@pytest.mark.parametrize(
    'path, index',
    [
        ('/films', 'movies'),
        ('/persons', 'persons'),
        ('/genres', 'genres'),
    ],
)
@pytest.mark.asyncio
async def test_get_list(
    path: str, index: str,  # args
    make_get_request: Callable, check_cache: Callable,  # fixtures
):
    """
    Test data retrieval.

    Args:
        path: URL path
        index: Elasticsearch index name
        make_get_request: Fixture for making HTTP requests
        check_cache: Fixture for checking data cache
    """
    response = await make_get_request(path)
    cache = await check_cache(index)

    assert response.status == http.HTTPStatus.OK
    assert cache
