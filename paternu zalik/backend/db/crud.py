from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.movie import MovieSchema, GenreSchema, Movie, Genre


async def create_movie(db: AsyncSession, movie: MovieSchema) -> Movie:
    """Create a new movie in favorites."""
    db_movie = Movie(
        movie_id=movie.movie_id,
        title=movie.title,
        overview=movie.overview,
        release_date=movie.release_date,
        vote_average=movie.vote_average,
        poster_path=movie.poster_path
    )
    
    try:
        db.add(db_movie)
        await db.commit()
        await db.refresh(db_movie)
        return db_movie
    except Exception as e:
        await db.rollback()
        raise e


async def get_movie(db: AsyncSession, movie_id: str) -> Optional[Movie]:
    """Get a movie by ID."""
    try:
        result = await db.execute(select(Movie).filter(Movie.movie_id == movie_id))
        return result.scalar_one_or_none()
    except Exception as e:
        await db.rollback()
        raise e


async def get_all_movies(db: AsyncSession) -> List[Movie]:
    """Get all favorite movies."""
    try:
        result = await db.execute(select(Movie))
        return result.scalars().all()
    except Exception as e:
        await db.rollback()
        raise e


async def delete_movie(db: AsyncSession, movie_id: str) -> bool:
    """Delete a movie from favorites."""
    try:
        db_movie = await get_movie(db, movie_id)
        if db_movie:
            await db.delete(db_movie)
            await db.commit()
            return True
        return False
    except Exception as e:
        await db.rollback()
        raise e


async def create_genre(db: AsyncSession, genre: GenreSchema) -> Genre:
    """Create a new genre."""
    db_genre = Genre(
        genre_id=genre.genre_id,
        name=genre.name
    )
    
    try:
        db.add(db_genre)
        await db.commit()
        await db.refresh(db_genre)
        return db_genre
    except Exception as e:
        await db.rollback()
        raise e


async def get_genre(db: AsyncSession, genre_id: str) -> Optional[Genre]:
    """Get a genre by ID."""
    try:
        result = await db.execute(select(Genre).filter(Genre.genre_id == genre_id))
        return result.scalar_one_or_none()
    except Exception as e:
        await db.rollback()
        raise e


async def get_all_genres(db: AsyncSession) -> List[Genre]:
    """Get all genres."""
    try:
        result = await db.execute(select(Genre))
        return result.scalars().all()
    except Exception as e:
        await db.rollback()
        raise e


async def delete_genre(db: AsyncSession, genre_id: str) -> bool:
    """Delete a genre."""
    try:
        db_genre = await get_genre(db, genre_id)
        if db_genre:
            await db.delete(db_genre)
            await db.commit()
            return True
        return False
    except Exception as e:
        await db.rollback()
        raise e
