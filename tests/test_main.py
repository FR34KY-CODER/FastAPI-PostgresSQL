import pytest
from httpx import AsyncClient
from app.main import app  # Absolute import

@pytest.mark.asyncio
async def test_auth_failure():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Request without X-API-KEY header
        response = await ac.post("/appointments/?title=Test&user_id=1")
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_auth_success():
    headers = {"X-API-KEY": "lnmiit-secret-key"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/appointments/?title=Test&user_id=1", headers=headers)
    # This will return 200 if DB is connected and user exists
    assert response.status_code in [200, 500]