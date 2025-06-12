import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_registration():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/accounts/register", json={
            "email": "test@example.com",
            "password": "testpassword123"
        })
        assert resp.status_code == 200 or resp.status_code == 409
