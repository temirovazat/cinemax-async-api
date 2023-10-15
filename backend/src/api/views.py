from typing import List

from fastapi import APIRouter, Depends

from api.v1.films import get_film_details, get_film_list, get_film_search
from api.v1.genres import get_genre_details, get_genre_list
from api.v1.persons import get_person_details, get_person_films, get_person_list, get_person_search
from models.film import Film, FilmList, FilmModified
from models.genre import Genre, GenreList
from models.person import Person, PersonList
from services.list import ListService
from services.retrieve import RetrieveService

router = APIRouter()


@router.get(
    '/films',
    response_model=FilmList,
    response_model_by_alias=False,
    summary='Homepage',
    description='Popular movies and filtering by genres',
    response_description='Movie titles and ratings',
    tags=['films'])
async def films(films_list: ListService = Depends(get_film_list)) -> List[FilmModified]:
    return await films_list.get()


@router.get(
    '/films/search',
    response_model=FilmList,
    response_model_by_alias=False,
    summary='Search Movies',
    description='Full-text search by movie titles',
    response_description='Movie titles and ratings',
    tags=['films'])
async def films_search(films_by_search: ListService = Depends(get_film_search)) -> List[FilmModified]:
    return await films_by_search.get()


@router.get(
    '/films/{film_id}',
    response_model=Film,
    response_model_by_alias=False,
    summary='Movie Page',
    description='Complete information about the movie',
    response_description='Movie title, description, rating, genres, and movie personnel',
    tags=['films'])
async def films_pk(film_details: RetrieveService = Depends(get_film_details)) -> Film:
    return await film_details.get()


@router.get(
    '/persons',
    response_model=PersonList,
    response_model_by_alias=False,
    summary='Persons',
    description='List of individuals',
    response_description='Full name, primary role, and movies involving the person',
    tags=['persons'])
async def persons(persons_list: ListService = Depends(get_person_list)) -> List[Person]:
    return await persons_list.get()


@router.get(
    '/persons/search',
    response_model=PersonList,
    response_model_by_alias=False,
    summary='Search Persons',
    description='Full-text search by individual names',
    response_description='Full name, primary role, and movies involving the person',
    tags=['persons'])
async def persons_search(persons_by_search: ListService = Depends(get_person_search)) -> List[Person]:
    return await persons_by_search.get()


@router.get(
    '/persons/{person_id}',
    response_model=Person,
    response_model_by_alias=False,
    summary='Person Page',
    description='Complete information about the individual',
    response_description='Full name, primary role, and movies involving the person',
    tags=['persons'])
async def persons_pk(person_details: RetrieveService = Depends(get_person_details)) -> Person:
    return await person_details.get()


@router.get(
    '/persons/{person_id}/film',
    response_model=FilmList,
    response_model_by_alias=False,
    summary='Movies by Person',
    description='Movies involving the individual, sorted by popularity',
    response_description='Movie titles and ratings for movies involving the person',
    tags=['persons'])
async def persons_pk_film(films_by_person: ListService = Depends(get_person_films)) -> List[FilmModified]:
    return await films_by_person.get()


@router.get(
    '/genres',
    response_model=GenreList,
    response_model_by_alias=False,
    summary='Genres',
    description='List of genres',
    response_description='Genre names and descriptions',
    tags=['genres'])
async def genres(genres_list: ListService = Depends(get_genre_list)) -> List[Genre]:
    return await genres_list.get()


@router.get(
    '/genres/{genre_id}',
    response_model=Genre,
    response_model_by_alias=False,
    summary='Genre Page',
    description='Complete information about the genre',
    response_description='Genre name and description',
    tags=['genres'])
async def genres_pk(genre_details: RetrieveService = Depends(get_genre_details)) -> Genre:
    return await genre_details.get()
