from typing import Dict, List, Optional, Type

from pydantic import BaseModel

from services.filters import FilterFilms, QuerySearch
from core.config import CinemaObject
from db import queries
from models.film import Film
from models.person import Person, RoleChoices


class SingleObjectMixin(BaseModel):
    """Mixin for generating a movie theater object from Elasticsearch database."""

    async def get_object(self, data: Dict, model: Type[CinemaObject]) -> CinemaObject:
        """
        Retrieve object and fetch data from other Elasticsearch indexes for the corresponding model.

        Args:
            data: Data to be processed
            model: The model for which the object should be retrieved

        Returns:
            CinemaObject: Movie theater object
        """
        if model == Film:
            data.update(await self.add_to_film(data))
        elif model == Person:
            data.update(await self.add_to_person(data))
        return model(uuid=data['id'], **data)

    async def add_to_film(self, film: Dict) -> Dict:
        """
        Add genre and director information to the movie data from the appropriate indexes.

        Args:
            film (Dict): Movie data.

        Returns:
            Dict: Movie genres and directors.
        """
        genres = await self.search_elastic_docs(  # type: ignore[attr-defined]
            index='genres', queryset={'body': queries.genres_by_film(film)},
        )
        directors = await self.search_elastic_docs(  # type: ignore[attr-defined]
            index='persons', queryset={'body': queries.directors_by_film(film)},
        )
        return {'genre': genres, 'directors': directors}

    async def add_to_person(self, person: Dict) -> Dict:
        """
        Add information about the persona's role and the movies related to the persona.

        Args:
            person: Persona data

        Returns:
            Dict: Role and IDs of movies featuring the persona
        """
        films = await self.search_elastic_docs(  # type: ignore[attr-defined]
            index='movies', queryset={'body': queries.films_by_person(
                person, fields=['id', 'actors_names', 'writers_names', 'director'],
            )},
        )
        return {
            'film_ids': [film['id'] for film in films],
            'role': self.parse_role(person['full_name'], films),
        }

    def parse_role(self, person_name: str, films: List[Dict]) -> str:
        """
        Process movies featuring a persona to determine their primary role.

        Args:
            person_name: Full name of the person
            films: List of movies with the person

        Returns:
            str: The persona's role that occurs most in movies featuring them
        """
        person_roles = [
            RoleChoices[role].value
            for film in films if film.pop('id')
            for role, names in film.items() if person_name in names
        ]
        return max(person_roles, key=person_roles.count, default='')


class QuerysetMixin(BaseModel):
    """Mixin for forming a query to ElasticSearch database."""

    filter: Optional[FilterFilms]
    page_number: Optional[int]
    page_size: Optional[int]
    query: Optional[QuerySearch]
    sort: Optional[str]

    def get_queryset(self) -> Dict:
        """
        Create a query to retrieve data from Elasticsearch.

        Returns:
            Dict: Query with data sorting
        """
        queryset: Dict = {}
        if self.sort:
            queryset.update(
                sort=f'{self.sort[1:]}:desc' if self.sort.startswith('-') else self.sort,
            )
        return queryset

    async def filter_queryset(self, queryset: Dict) -> Dict:
        """
        Add parameters to a query for data filtering or full-text search.

        Args:
            queryset (Dict): Query in Elasticsearch

        Returns:
            Dict: Query with data filtering or searching
        """
        if self.filter:
            queryset.update(
                body=await self.filter.get_query(service=self),  # type: ignore[arg-type]
            )
        elif self.query:
            queryset.update(
                body=queries.search_data(query_str=str(self.query), fields=self.query.fields),
            )
        return queryset

    def paginate_queryset(self, queryset: Dict) -> Dict:
        """
        Adding parameters to the query to paginate theater objects.

        Args:
            queryset (Dict): Query in Elasticsearch

        Returns:
            Dict: Query with page retrieval
        """
        if (page := self.page_number) and (size := self.page_size):
            queryset.update(
                from_=(page - 1) * size if page > 1 else 0,
                size=size,
            )
        return queryset
