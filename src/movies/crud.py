from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Movie
from .schemas import MovieCreateSchema

async def get_movies(session: AsyncSession, skip=0, limit=10):
    result = await session.execute(select(Movie).offset(skip).limit(limit))
    return result.scalars().all()

async def get_movie_by_id(session: AsyncSession, movie_id: int):
    result = await session.execute(select(Movie).where(Movie.id == movie_id))
    return result.scalar_one_or_none()

async def create_movie(session: AsyncSession, movie_data: MovieCreateSchema):
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
    # TODO: genres, directors, stars
    session.add(movie)
    await session.commit()
    await session.refresh(movie)
    return movie
