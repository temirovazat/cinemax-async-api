from typing import Iterator, List, Union

from faker import Faker

from testdata.schemas.genre import Genre
from testdata.schemas.person import Person
from testdata.schemas.movie import PersonInMovie, Movie
from conftest import GENRES, MOVIES_PER_GENRE, ACTORS_PER_MOVIE, WRITERS_PER_MOVIE


class ElasticDocsFactory:
    """Class for generating Elasticsearch documents."""

    SCHEMAS = Movie, Person, Genre

    def __init__(self) -> None:
        """Upon class initialization, create a fake data generation object."""
        self.fake = Faker()

    @property
    def fake_movie_person(self) -> PersonInMovie:
        """
        Document for a person in a movie.

        Returns:
            PersonInMovie: Document for a person in a movie.
        """
        return PersonInMovie(id=self.fake.uuid4(), name=self.fake.name())

    def get_movies(self, genre: Genre) -> Iterator[Movie]:
        """
        Generate movies as documents with a given genre.

        Args:
            genre: Genre

        Yields:
            Movie: Movie document.
        """
        for _ in range(MOVIES_PER_GENRE):
            actors = [self.fake_movie_person for _ in range(ACTORS_PER_MOVIE)]
            writers = [self.fake_movie_person for _ in range(WRITERS_PER_MOVIE)]
            yield Movie(
                id=self.fake.uuid4(),
                imdb_rating=self.fake.pyfloat(positive=True, right_digits=1, max_value=10),
                genre=[genre.name],
                title=' '.join(word.capitalize() for word in self.fake.words()),
                description=self.fake.text(),
                director=[self.fake.name()],
                actors_names=[actor.name for actor in actors],
                writers_names=[writer.name for writer in writers],
                actors=actors,
                writers=writers,
            )

    def get_persons(self, movie: Movie) -> Iterator[Person]:
        """
        Generate persons from a movie as documents.

        Args:
            movie: Movie

        Yields:
            Person: Person document.
        """
        for person in sum([list(movie.actors), list(movie.writers)], []):
            yield Person(id=person.id, full_name=person.name)
        yield Person(id=self.fake.uuid4(), full_name=movie.director[0])

    def get_genres(self, genres_names: List[str]) -> Iterator[Genre]:
        """
        Generate genres as documents.

        Args:
            genres_names: Genre names.

        Yields:
            Genre: Genre document.
        """
        for name in genres_names:
            yield Genre(id=self.fake.uuid4(), name=name, description=self.fake.text())

    def gendata(self) -> Iterator[Union[Movie, Person, Genre]]:
        """
        Generate Elasticsearch documents as the main process.

        Yields:
            Movie | Person | Genre: Fake cinema documents.
        """
        for genre in self.get_genres(GENRES):
            for movie in self.get_movies(genre):
                yield genre
                yield movie
                yield from self.get_persons(movie)
