from typing import AsyncGenerator, Callable, Dict, List, Union

import aiohttp
import jwt
import pytest
import pytest_asyncio
from multidict import CIMultiDictProxy
from pydantic import BaseModel

from settings import TEST_CONFIG, QueryParams


class HttpResponse(BaseModel):
    """Class representing the server's HTTP response to a client request."""
    
    body: Union[Dict, List[Dict]]
    headers: CIMultiDictProxy
    status: int

    class Config:
        arbitrary_types_allowed = True


@pytest_asyncio.fixture(scope='session')
async def session() -> AsyncGenerator[aiohttp.ClientSession, None]:
    """
    Fixture for creating an HTTP session between the server and the client.

    Yields:
        aiohttp.ClientSession: An object for asynchronous HTTP interaction.
    """
    token = jwt.encode({'some': 'payload'}, TEST_CONFIG.secret_key, algorithm='HS256')
    session = aiohttp.ClientSession(headers={'Authorization': f'Bearer {token}'})
    try:
        yield session
    finally:
        await session.close()


def get_url_path(path: str) -> str:
    """
    Get the URL of a resource without query parameters.

    Args:
        path: Path to the resource.

    Returns:
        str: URL of the resource.
    """
    return '{url}{path_to_resource}'.format(url=TEST_CONFIG.url, path_to_resource=path)


def get_query_params(**params) -> Dict:
    """
    Get and format query parameters for a URL.

    Args:
        params: Named query parameters.

    Returns:
        Dict: Query parameters in the URL.
    """
    return QueryParams(**params).dict(by_alias=True, exclude_none=True)


@pytest.fixture(scope='session')
def make_get_request(session: aiohttp.ClientSession) -> Callable:
    """
    Fixture with a nested function for fetching data from the server.

    Args:
        session: Fixture with an HTTP client.

    Returns:
        Callable: Fixture function to fetch data from the HTTP server.
    """
    async def inner(path: str, **params) -> HttpResponse:
        async with session.get(
            url=get_url_path(path=path),
            params=get_query_params(**params),
        ) as response:
            return HttpResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )
    return inner
