import pytest

@pytest.mark.asyncio
async def test_cart_lifecycle(async_client):
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
