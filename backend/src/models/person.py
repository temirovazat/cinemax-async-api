from enum import Enum
from typing import ClassVar, List
from uuid import UUID

from models.base import OrjsonMixin, UUIDMixin


class RoleChoices(Enum):
    """An auxiliary model for matching the field name in Elasticsearch with the persona role."""

    actors_names = 'actor'
    writers_names = 'writer'
    director = 'director'


class Person(UUIDMixin, OrjsonMixin):
    """A model persona with a major role and movies with him in it."""

    full_name: str
    role: str
    film_ids: List[UUID]


class PersonList(OrjsonMixin):
    """A model for parsing a list of persons with information about their roles and movies."""

    __root__: List[Person]
    item: ClassVar[type] = Person
