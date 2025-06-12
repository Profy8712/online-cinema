import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_place_order():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/orders/", json={"movie_ids": [1, 2]})
        assert resp.status_code in (200, 400)

@pytest.mark.asyncio
async def test_get_order_not_found():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/orders/99999")
        assert resp.status_code == 404
