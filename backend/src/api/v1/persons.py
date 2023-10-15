from functools import lru_cache

from fastapi import Depends, Path, Query

from api.v1.base import Database, Paginator
from services.filters import FilterPersonFilms, QuerySearch
from services.list import ListService
from services.retrieve import RetrieveService
from models.film import FilmList
from models.person import Person, PersonList


@lru_cache()
def get_person_list(
    paginator: Paginator = Depends(),
    database: Database = Depends(),
) -> ListService:
    """
    Retrieve a list of persons using the ListService provider.

    Args:
        paginator: Paginator
        database: Database connections

    Returns:
        ListService: Service for retrieving a list of cinema objects
    """
    return ListService(
        elastic=database.elastic, redis=database.redis,
        index='persons', model=PersonList,
        page_size=paginator.size, page_number=paginator.page,
    )


@lru_cache()
def get_person_search(
    query: str = Query(default=None, description='Search query'),
    paginator: Paginator = Depends(),
    database: Database = Depends(),
) -> ListService:
    """
    Retrieve search results for persons using the ListService provider function.

    Args:
        query: Search query
        paginator: Paginator
        database: Database connections

    Returns:
        ListService: Service for retrieving a list of cinema objects
    """
    return ListService(
        elastic=database.elastic, redis=database.redis,
        index='persons', model=PersonList,
        page_size=paginator.size, page_number=paginator.page,
        query=QuerySearch(q_string=query, fields=['full_name']),
    )


@lru_cache()
def get_person_films(
    person_id: str = Path(title='Person ID'),
    database: Database = Depends(),
) -> ListService:
    """
    Retrieve films associated with a person using ListService.

    Args:
        person_id (str): Person ID for filtering films
        database (Database): Database connections

    Returns:
        ListService: Service for retrieving a list of cinema objects
    """
    return ListService(
        elastic=database.elastic, redis=database.redis,
        index='movies', model=FilmList,
        filter=FilterPersonFilms(person_id=person_id),
    )


@lru_cache()
def get_person_details(
    person_id: str = Path(title='Person ID'),
    database: Database = Depends(),
) -> RetrieveService:
    """
    Retrieve a person by ID using the RetrieveService.

    Args:
        person_id: Person ID
        database: Database connections

    Returns:
        RetrieveService: Service for retrieving a cinema object by ID
    """
    return RetrieveService(
        elastic=database.elastic, redis=database.redis,
        index='persons', model=Person, id=person_id,
    )
