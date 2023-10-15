from functools import lru_cache

from fastapi import Depends, Path, Query

from api.v1.base import Database, Paginator
from services.filters import FilterGenreFilms, QuerySearch
from services.list import ListService
from services.retrieve import RetrieveService
from models.film import Film, FilmList


@lru_cache()
def get_film_list(
    filter_genre: str = Query(default=None, alias='filter[genre]', description='Filter by genre'),
    sort: str = Query(default=None, description='Sorting parameter'),
    paginator: Paginator = Depends(),
    database: Database = Depends(),
) -> ListService:
    """
    Retrieve a list of films using the ListService provider.

    Args:
        filter_genre: Filter films by genre.
        sort: Specify the sorting parameter.
        paginator: Pagination settings.
        database: Database connections.

    Returns:
        ListService: A service for obtaining a list of cinema objects.
    """
    return ListService(
        elastic=database.elastic, redis=database.redis,
        index='movies', model=FilmList,
        filter=FilterGenreFilms(genre_id=filter_genre),
        page_size=paginator.size, page_number=paginator.page, sort=sort,
    )


@lru_cache()
def get_film_search(
    query: str = Query(default=None, description='Search query'),
    paginator: Paginator = Depends(),
    database: Database = Depends(),
) -> ListService:
    """
    Retrieve search results for films using ListService.

    Args:
        query: Search query
        paginator: Paginator
        database: Database connections

    Returns:
        ListService: Service for obtaining a list of cinema objects
    """
    return ListService(
        elastic=database.elastic, redis=database.redis,
        index='movies', model=FilmList,
        page_size=paginator.size, page_number=paginator.page,
        query=QuerySearch(q_string=query, fields=['title']),
    )


@lru_cache()
def get_film_details(
    film_id: str = Path(title='Film ID'),
    database: Database = Depends(),
) -> RetrieveService:
    """
    Retrieve film details by Film ID using the RetrieveService.

    Args:
        film_id (str): Film ID
        database (Database): Database connections

    Returns:
        RetrieveService: Service for retrieving a cinema object by ID
    """
    return RetrieveService(
        elastic=database.elastic, redis=database.redis,
        index='movies', model=Film, id=film_id,
    )
