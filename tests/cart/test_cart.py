import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_cart_lifecycle():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Get empty cart
        resp = await ac.get("/cart/")
        assert resp.status_code == 200

        # Add movie to cart
        resp = await ac.post("/cart/add", json={"movie_id": 1})
        assert resp.status_code == 200

        # Remove movie from cart
        resp = await ac.post("/cart/remove", json={"movie_id": 1})
        assert resp.status_code == 200

        # Clear cart
        resp = await ac.post("/cart/clear")
        assert resp.status_code == 200
