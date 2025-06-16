import pytest


@pytest.mark.asyncio
async def test_cart_lifecycle(async_client, async_session_maker):
    # Create a test movie in the database
    from src.movies.models import Movie  # Adjust import if needed
    async with async_session_maker() as session:
        movie = Movie(id=1, title="Test Movie")  # Add other required fields
        session.add(movie)
        await session.commit()

    # Get empty cart
    resp = await async_client.get("/cart/")
    assert resp.status_code == 200

    # Add movie to cart
    resp = await async_client.post("/cart/add", json={"movie_id": 1})
    assert resp.status_code == 200

    # Remove movie from cart
    resp = await async_client.post("/cart/remove", json={"movie_id": 1})
    assert resp.status_code == 200

    # Clear cart
    resp = await async_client.post("/cart/clear")
    assert resp.status_code == 200
