from functools import lru_cache

from fastapi import Depends, Path

from api.v1.base import Database, Paginator
from services.list import ListService
from services.retrieve import RetrieveService
from models.genre import Genre, GenreList


@lru_cache()
def get_genre_list(
    paginator: Paginator = Depends(),
    database: Database = Depends(),
) -> ListService:
    """
    Retrieve a list of genres using the ListService.

    Args:
        paginator (Paginator): The pagination settings.
        database (Database): Database connections.

    Returns:
        ListService: A service for fetching a list of cinema objects.
    """
    return ListService(
        elastic=database.elastic, redis=database.redis,
        index='genres', model=GenreList,
        page_size=paginator.size, page_number=paginator.page,
    )


@lru_cache()
def get_genre_details(
    genre_id: str = Path(title='Genre ID'),
    database: Database = Depends(),
) -> RetrieveService:
    """
    Get a genre's details by its ID.

    Args:
        genre_id: Genre ID
        database: Database connections

    Returns:
        RetrieveService: Service for retrieving a cinema object by ID
    """
    return RetrieveService(
        elastic=database.elastic, redis=database.redis,
        index='genres', model=Genre, id=genre_id,
    )
