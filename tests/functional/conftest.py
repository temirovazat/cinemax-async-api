from testdata.schemas.genre import GENRES

MOVIES_PER_GENRE = 5
ACTORS_PER_MOVIE = 5
WRITERS_PER_MOVIE = 2
DIRECTOR = 1

GENRES_COUNT = len(GENRES)
MOVIES_COUNT = MOVIES_PER_GENRE * GENRES_COUNT
PERSONS_COUNT = (ACTORS_PER_MOVIE + WRITERS_PER_MOVIE + DIRECTOR) * MOVIES_COUNT

pytest_plugins = [
    'functional.src.fixtures.fixture_loop',
    'functional.src.fixtures.fixture_elastic',
    'functional.src.fixtures.fixture_redis',
    'functional.src.fixtures.fixture_session',
]
