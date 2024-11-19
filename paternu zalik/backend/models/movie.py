from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import Column, String, DateTime, Text, Float
from backend.db.database import Base


class MovieSchema(BaseModel):
    movie_id: str
    title: str
    overview: str
    release_date: str
    vote_average: float
    poster_path: Optional[str] = None

    class Config:
        from_attributes = True


class GenreSchema(BaseModel):
    genre_id: int
    name: str

    class Config:
        from_attributes = True


class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(String(50), primary_key=True)
    title = Column(String(200), nullable=False)
    overview = Column(Text, nullable=False)
    release_date = Column(String(50))
    vote_average = Column(Float)
    poster_path = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Movie {self.title}>"


class Genre(Base):
    __tablename__ = "genres"

    genre_id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Genre {self.name}>" 