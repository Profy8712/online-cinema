import pytest

@pytest.mark.asyncio
async def test_place_order(async_client):
    resp = await async_client.post("/orders/", json={"movie_ids": [1, 2]})
    # 200 если заказ успешно создан, 400 если переданы неверные данные
    assert resp.status_code in (200, 400)

@pytest.mark.asyncio
async def test_get_order_not_found(async_client):
    resp = await async_client.get("/orders/99999")
    assert resp.status_code == 404
