import abc
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from services.base import BaseService
from db import queries


class BaseFilter(BaseModel, abc.ABC):
    """Abstract class for cinema data filter."""

    def __new__(cls, **kwargs):
        """
        When creating an object, return None if there is no data for filtering.

        Args:
            kwargs: Named arguments for object creation

        Returns:
            Optional['BaseFilter']: Filter object or None
        """
        return super().__new__(cls) if all(kwargs.values()) else None


class FilterFilms(BaseFilter):
    """Abstract class for film filters."""

    id: Optional[UUID]

    @abc.abstractmethod
    async def get_query(self, service: BaseService) -> Dict:
        """Retrieve data and query for filtering data.

        Args:
            service: Service performing business logic with films
        """

    def __str__(self) -> str:
        """
        Return the string representation of the object's ID for filtering.

        Returns:
            str: The ID of the object for filtering
        """
        return str(self.id)


class FilterGenreFilms(FilterFilms):
    """Class for filtering films by genre."""

    id: Optional[UUID] = Field(alias='genre_id')

    async def get_query(self, service: BaseService) -> Dict:
        """
        Retrieve genre data and query for filtering films by it.

        Args:
            service: Service performing business logic with films

        Returns:
            Dict: Query with genre filtering
        """
        genre = await service.get_elastic_doc(index='genres', doc_id=self.id)
        return queries.films_by_genre(genre)


class FilterPersonFilms(FilterFilms):
    """Class for filtering films by a person."""

    id: Optional[UUID] = Field(alias='person_id')

    async def get_query(self, service: BaseService) -> Dict:
        """
        Retrieve person data and query for filtering films by them.

        Args:
            service: Service performing business logic with films

        Returns:
            Dict: Query with person filtering
        """
        person = await service.get_elastic_doc(index='persons', doc_id=self.id)
        return queries.films_by_person(person, fields=['id', 'title', 'imdb_rating'])


class QuerySearch(BaseFilter):
    """Class for full-text data search filter."""

    q_string: Optional[str]
    fields: List[str] = Field(default_factory=list)

    def __str__(self) -> str:
        """
        Return the search query string as the provided search string.

        Returns:
            str: The search query string
        """
        return self.q_string or ''
