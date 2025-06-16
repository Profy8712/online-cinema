import pytest

@pytest.mark.asyncio
async def test_registration(async_client):
    resp = await async_client.post("/accounts/register", json={
        "email": "test@example.com",
        "password": "testpassword123"
    })
    assert resp.status_code in (200, 201, 409)
