from sqlalchemy import (
    Column, Integer, String, Float, ForeignKey, Text, Table, DECIMAL, UniqueConstraint
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

# Association Tables
movie_genres = Table(
    "movie_genres", Base.metadata,
    Column("movie_id", ForeignKey("movies.id"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id"), primary_key=True)
)

movie_directors = Table(
    "movie_directors", Base.metadata,
    Column("movie_id", ForeignKey("movies.id"), primary_key=True),
    Column("director_id", ForeignKey("directors.id"), primary_key=True)
)

movie_stars = Table(
    "movie_stars", Base.metadata,
    Column("movie_id", ForeignKey("movies.id"), primary_key=True),
    Column("star_id", ForeignKey("stars.id"), primary_key=True)
)

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class Star(Base):
    __tablename__ = "stars"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class Director(Base):
    __tablename__ = "directors"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class Certification(Base):
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class Movie(Base):
    __tablename__ = "movies"
    __table_args__ = (
        UniqueConstraint('name', 'year', 'time', name='uq_movie_name_year_time'),
    )

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4, nullable=False)
    name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    time = Column(Integer, nullable=False)
    imdb = Column(Float, nullable=False)
    votes = Column(Integer, nullable=False)
    meta_score = Column(Float)
    gross = Column(Float)
    description = Column(Text, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    certification_id = Column(Integer, ForeignKey("certifications.id"), nullable=False)

    certification = relationship("Certification")
    genres = relationship("Genre", secondary=movie_genres, backref="movies")
    directors = relationship("Director", secondary=movie_directors, backref="movies")
    stars = relationship("Star", secondary=movie_stars, backref="movies")
