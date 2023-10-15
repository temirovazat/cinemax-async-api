from typing import Callable, Dict, List

import pytest


def persons_names(film: Dict) -> List[str]:
    """
    Get a list of persons' names in the film.

    Args:
        film: Film with persons

    Returns:
        list[str]: List of persons' names
    """
    return film['actors_names'] + film['writers_names'] + film['director']


def genres_names(film: Dict) -> List[str]:
    """
    Get a list of film genres' names.

    Args:
        film: Film with genres

    Returns:
        list[str]: List of genre names
    """
    return film['genre']


@pytest.mark.parametrize(
    'path, index, check_field, check_list',
    [
        ('/films?filter[genre]={id}', 'genres', 'name', genres_names),
        ('/persons/{id}/film', 'persons', 'full_name', persons_names),
    ],
)
@pytest.mark.asyncio
async def test_films_filters(
    path: str, index: str, check_field: str, check_list: Callable,  # args
    extract_data: Callable, make_get_request: Callable,  # fixtures
):
    """
    Test filters for films.

    Args:
        path: URL resource path
        index: Elasticsearch index name
        check_field: Object field used for filtering
        check_list: Function returning a list to check the object's presence
        extract_data: Fixture for extracting data from the database
        make_get_request: Fixture for making an HTTP request
    """
    expected = await extract_data(index)

    response = await make_get_request(path=path.format(id=expected['id']))
    film = await extract_data(index='movies', id=response.body[0]['uuid'])

    assert expected[check_field] in check_list(film)
