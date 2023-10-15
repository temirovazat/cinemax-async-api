from typing import ClassVar, List, Type
from uuid import UUID

from pydantic import BaseModel, Field

from models.base import OrjsonMixin, UUIDMixin


class GenreInFilm(BaseModel):
    """A model of the genre in the movie."""

    uuid: UUID = Field(alias='id')
    name: str

    class Config(OrjsonMixin.Config):
        """Validation Settings."""

        allow_population_by_field_name = True


class PersonInFilm(BaseModel):
    """A model of the persona in the movie."""

    uuid: UUID = Field(alias='id')
    full_name: str = Field(alias='name')

    class Config(OrjsonMixin.Config):
        """Validation Settings."""

        allow_population_by_field_name = True


class Film(UUIDMixin, OrjsonMixin):
    """A model of the movie with complete information."""

    title: str
    imdb_rating: float
    description: str
    genre: List[GenreInFilm]
    actors: List[PersonInFilm]
    writers: List[PersonInFilm]
    directors: List[PersonInFilm]


class FilmModified(UUIDMixin, OrjsonMixin):
    """A model of the movie with brief information."""

    title: str
    imdb_rating: float


class FilmList(OrjsonMixin):
    """A model for parsing a list of movies with brief information."""

    __root__: List[FilmModified]
    item: ClassVar[Type] = FilmModified
