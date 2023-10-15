from elasticsearch_dsl import Float, InnerDoc, Keyword, MetaField, Nested, Text

from testdata.schemas.base import Mappings, Settings


class PersonInMovie(InnerDoc):
    """Class representing a nested document structure containing information about a person in a movie."""

    id = Keyword()
    name = Text(analyzer='ru_en')

    class Meta:
        dynamic = MetaField('strict')


class Movie(Mappings):
    """Class representing a document structure containing information about a movie."""

    imdb_rating = Float()
    genre = Keyword()
    title = Text(analyzer='ru_en', fields={'raw': Keyword()})
    description = Text(analyzer='ru_en')
    director = Text(analyzer='ru_en')
    actors_names = Text(analyzer='ru_en')
    writers_names = Text(analyzer='ru_en')
    actors = Nested(PersonInMovie)
    writers = Nested(PersonInMovie)

    class Index(Settings):
        name = 'movies'
