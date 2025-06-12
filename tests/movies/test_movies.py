import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_list_movies():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/movies/")
        assert resp.status_code == 200

@pytest.mark.asyncio
async def test_movie_detail_not_found():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/movies/999999")
        assert resp.status_code == 404
