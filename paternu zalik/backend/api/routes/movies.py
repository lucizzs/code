"""Module for handling movie-related API endpoints."""

import httpx
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from backend.db.database import get_session
from backend.models.movie import MovieSchema, GenreSchema, Movie, Genre
from backend.db.crud import (
    get_movie, create_movie, get_all_movies,
    delete_movie, get_genre, create_genre, 
    get_all_genres, delete_genre
)
from backend.builders.movie_builder import MovieBuilder
from backend.factories.response_factory import APIResponseFactory
from backend.config import TMDB_API_KEY

movies_router = APIRouter(include_in_schema=True)

TMDB_API_URL = "https://api.themoviedb.org/3"


@movies_router.get("/popular/")
async def get_popular_movies() -> List[Dict[str, Any]]:
    """Fetches popular movies from TMDB API."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{TMDB_API_URL}/movie/popular",
            params={"api_key": TMDB_API_KEY}
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Error fetching popular movies"
            )
        return response.json()["results"]


@movies_router.post("/favorites/", response_model=MovieSchema)
async def save_favorite_movie(
    movie: MovieSchema,
    db: AsyncSession = Depends(get_session)
) -> Movie:
    """Saves a movie to favorites."""
    return await create_movie(db, movie)


@movies_router.get("/favorites/", response_model=List[MovieSchema])
async def get_favorite_movies(
    db: AsyncSession = Depends(get_session)
) -> List[Movie]:
    """Retrieves all favorite movies."""
    movies = await get_all_movies(db)
    if not movies:
        raise HTTPException(404, "No favorite movies found")
    return movies


@movies_router.delete("/favorites/{movie_id}")
async def delete_favorite_movie(
    movie_id: str,
    db: AsyncSession = Depends(get_session)
) -> Dict[str, str]:
    """Removes a movie from favorites."""
    deleted = await delete_movie(db, movie_id)
    if not deleted:
        raise HTTPException(404, "Movie not found")
    return {"message": "Movie removed from favorites"}


@movies_router.get("/search/{query}")
async def search_movies(query: str) -> Dict[str, Any]:
    """Searches for movies in TMDB API."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{TMDB_API_URL}/search/movie",
            params={
                "api_key": TMDB_API_KEY,
                "query": query
            }
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Error searching movies"
            )
        return response.json() 