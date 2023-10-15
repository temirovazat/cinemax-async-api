from typing import ClassVar, List

from models.base import OrjsonMixin, UUIDMixin


class Genre(UUIDMixin, OrjsonMixin):
    """A model of the genre."""

    name: str
    description: str


class GenreList(OrjsonMixin):
    """A model for parsing a list of genres."""

    __root__: List[Genre]
    item: ClassVar[type] = Genre
