import pytest

@pytest.mark.asyncio
async def test_create_checkout_session(async_client):
    resp = await async_client.post("/payments/checkout-session", json={
        "order_id": 1,
        "amount": 19.99
    })
    assert resp.status_code in (200, 404)
    if resp.status_code == 200:
        assert "checkout_url" in resp.json()
