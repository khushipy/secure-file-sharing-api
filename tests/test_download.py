import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
@pytest.mark.skip(reason="Requires actual valid encrypted download URL")
async def test_download_file():
    encrypted_url = "gAAAA..."  

    async with AsyncClient(app=app, base_url="http://test") as ac:
        login = await ac.post("/auth/login", json={
            "email": "coco@example.com",
            "password": "coco123"
        })
        assert login.status_code == 200
        token = login.json()["access_token"]

        response = await ac.get(f"/download-file/{encrypted_url}",
                                headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
