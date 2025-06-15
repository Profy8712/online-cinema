import pytest

@pytest.mark.asyncio
async def test_list_movies(async_client):
    resp = await async_client.get("/movies/")
    assert resp.status_code == 200

@pytest.mark.asyncio
async def test_movie_detail_not_found(async_client):
    resp = await async_client.get("/movies/999999")
    assert resp.status_code == 404
