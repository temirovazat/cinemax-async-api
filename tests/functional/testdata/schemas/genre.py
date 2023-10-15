from elasticsearch_dsl import Keyword, Text

from testdata.schemas.base import Mappings, Settings

GENRES = (
    'Action',
    'Adventure',
    'Fantasy',
    'Sci-Fi',
    'Drama',
    'Music',
    'Romance',
    'Thriller',
    'Mystery',
    'Comedy',
    'Animation',
    'Family',
    'Biography',
    'Musical',
    'Crime',
    'Short',
    'Western',
    'Documentary',
    'History',
    'War',
    'Game-Show',
    'Reality-TV',
    'Horror',
    'Sport',
    'Talk-Show',
    'News',
)


class Genre(Mappings):
    """Class representing the document structure with genre data.

    Attributes:
        name (Text): The name of the genre.
        description (Text): The description of the genre.

    Index:
        name: 'genres'
    """

    name = Text(analyzer='ru_en', fields={'raw': Keyword()})
    description = Text(analyzer='ru_en')

    class Index(Settings):
        name = 'genres'
