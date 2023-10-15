from typing import Callable, List

import pytest


def asc(data: List[float]) -> bool:
    """
    Return `True` if the numbers in the list are in ascending order.

    Args:
        data: List of floating-point numbers

    Returns:
        bool: Boolean value
    """
    return all(prev <= next for prev, next in zip(data, data[1:]))


def desc(data: List[float]) -> bool:
    """
    Return `True` if the numbers in the list are in descending order.

    Args:
        data: List of floating-point numbers

    Returns:
        bool: Boolean value
    """
    return all(prev >= next for prev, next in zip(data, data[1:]))


@pytest.mark.parametrize(
    'sort, ordering',
    [
        ('imdb_rating', asc),
        ('-imdb_rating', desc),
    ],
)
@pytest.mark.asyncio
async def test_films_sorting(
    sort: str, ordering: Callable,  # args
    make_get_request: Callable,  # fixtures
):
    """
    Test film sorting by rating.

    Args:
        sort: Film field with its rating
        ordering: Function returning a boolean value for compliance with the order of elements
        make_get_request: Fixture that performs an HTTP request
    """
    response = await make_get_request(path='/films', sort=sort)
    sorted_by = sort[1:] if sort.startswith('-') else sort

    assert response.body
    assert ordering([film[sorted_by] for film in response.body])
