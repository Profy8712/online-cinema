import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_create_checkout_session():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/payments/checkout-session", json={
            "order_id": 1,
            "amount": 19.99
        })
        assert resp.status_code == 200
        assert "checkout_url" in resp.json()
