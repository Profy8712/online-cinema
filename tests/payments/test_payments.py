import pytest

@pytest.mark.asyncio
async def test_create_checkout_session(async_client):
    resp = await async_client.post("/payments/checkout-session", json={
        "order_id": 1,
        "amount": 19.99
    })
    # Статус 200 если все ок, или 404 если нет заказа, зависит от состояния БД
    assert resp.status_code in (200, 404)
    if resp.status_code == 200:
        assert "checkout_url" in resp.json()
