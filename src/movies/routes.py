from http.client import HTTPException

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_async_session
from .schemas import MovieSchema
from .crud import get_movies, get_movie_by_id

router = APIRouter(prefix="/movies", tags=["movies"])

@router.get("/", response_model=list[MovieSchema])
async def list_movies(
    skip: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(get_async_session)
):
    movies = await get_movies(session, skip=skip, limit=limit)
    return movies

@router.get("/{movie_id}", response_model=MovieSchema)
async def movie_detail(movie_id: int, session: AsyncSession = Depends(get_async_session)):
    movie = await get_movie_by_id(session, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie
