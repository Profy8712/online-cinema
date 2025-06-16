from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Movie, Genre, Director, Star, Certification
from .schemas import MovieCreateSchema

async def get_movies(session: AsyncSession, skip=0, limit=10):
    result = await session.execute(select(Movie).offset(skip).limit(limit))
    return result.scalars().all()

async def get_movie_by_id(session: AsyncSession, movie_id: int):
    result = await session.execute(select(Movie).where(Movie.id == movie_id))
    return result.scalar_one_or_none()

async def create_movie(session: AsyncSession, movie_data: MovieCreateSchema):
    # Create Movie instance
    movie = Movie(
        name=movie_data.name,
        year=movie_data.year,
        time=movie_data.time,
        imdb=movie_data.imdb,
        votes=movie_data.votes,
        meta_score=movie_data.meta_score,
        gross=movie_data.gross,
        description=movie_data.description,
        price=movie_data.price,
        certification_id=movie_data.certification_id
    )
    # Add movie to session first
    session.add(movie)
    await session.flush()  # flush to get movie.id for many-to-many

    # Link genres
    if movie_data.genre_ids:
        genres = await session.execute(select(Genre).where(Genre.id.in_(movie_data.genre_ids)))
        movie.genres = genres.scalars().all()

    # Link directors
    if movie_data.director_ids:
        directors = await session.execute(select(Director).where(Director.id.in_(movie_data.director_ids)))
        movie.directors = directors.scalars().all()

    # Link stars
    if movie_data.star_ids:
        stars = await session.execute(select(Star).where(Star.id.in_(movie_data.star_ids)))
        movie.stars = stars.scalars().all()

    await session.commit()
    await session.refresh(movie)
    return movie
