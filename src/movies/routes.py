from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_async_session
from .schemas import MovieSchema, MovieCreateSchema
from .crud import get_movies, get_movie_by_id, create_movie

router = APIRouter(prefix="/movies", tags=["movies"])

@router.get("/", response_model=list[MovieSchema])
async def list_movies(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)):
    return await get_movies(session, skip, limit)

@router.get("/{movie_id}", response_model=MovieSchema)
async def movie_detail(movie_id: int, session: AsyncSession = Depends(get_async_session)):
    movie = await get_movie_by_id(session, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.post("/", response_model=MovieSchema, status_code=status.HTTP_201_CREATED)
async def create_movie_endpoint(movie: MovieCreateSchema, session: AsyncSession = Depends(get_async_session)):
    try:
        new_movie = await create_movie(session, movie)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return new_movie
