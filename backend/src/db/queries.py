from typing import Dict, List, Optional

from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MatchPhrase, Nested, QueryString, Term, Terms


def genres_by_film(film: Dict) -> Dict:
    """
    Retrieve a query in Elasticsearch to fetch the genres of the provided movie.

    Args:
        film: Movie data

    Returns:
        Dict: Query to Elasticsearch for the movie's genres
    """
    query = Search().filter(Terms(name__raw=film['genre']))
    return query.to_dict()


def directors_by_film(film: Dict) -> Dict:
    """
    Retrieve the directors of the submitted movie by querying Elasticsearch.

    Args:
        film: movie data

    Returns:
        Dict: Query to Elasticsearch for the directors of the movie
    """
    query = Search().filter(Terms(full_name__raw=film['director']))
    return query.to_dict()


def films_by_person(person: Dict, fields: Optional[List] = None) -> Dict:
    """
    Retrieve a query in Elasticsearch to fetch movies related to the specified person.

    Args:
        person (Dict): Person data.
        fields (Optional[List]): Index fields in Elasticsearch with movie data.

    Returns:
        Dict: Elasticsearch query for the person's movies.
    """
    query = Search().source(fields).sort('-imdb_rating').filter(
        Nested(path='actors', query=Term(actors__id=person['id'])) |
        Nested(path='writers', query=Term(writers__id=person['id'])) |
        MatchPhrase(director=person['full_name']),
    )[:1000]
    return query.to_dict()


def films_by_genre(genre: Dict) -> Dict:
    """
    Retrieve a query in Elasticsearch to retrieve movies of the passed genre.

    Args:
        genre: Genre data

    Returns:
        Dict: Query to Elasticsearch for movies of the genre
    """
    query = Search().filter(Term(genre=genre['name']))
    return query.to_dict()


def search_data(query_str: str, fields: Optional[List] = None) -> Dict:
    """
    Retrieve a query in Elasticsearch for the purpose of full-text search.

    Args:
        query_str (str): Query for full-text search.
        fields (List, optional): Index fields to search in Elasticsearch.

    Returns:
        Dict: A query in Elasticsearch for full-text search purposes.
    """
    query = Search().filter(QueryString(query=query_str, fields=fields))
    return query.to_dict()
