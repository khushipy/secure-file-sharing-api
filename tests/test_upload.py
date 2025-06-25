import pytest
from httpx import AsyncClient
from app.main import app
from pathlib import Path

@pytest.mark.asyncio
async def test_upload_file_as_ops():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Login as ops
        login = await ac.post("/auth/login", json={
            "email": "ironman@example.com",
            "password": "ironman123"
        })
        assert login.status_code == 200
        token = login.json()["access_token"]

        # Upload file
        test_file = Path("tests/mnt/data/sample.xlsx")
        assert test_file.exists(), f"File not found: {test_file}"

        with open(test_file, "rb") as f:
            response = await ac.post(
                "/upload",
                files={"file": ("sample.xlsx", f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
                headers={"Authorization": f"Bearer {token}"}
            )
        assert response.status_code == 200
        assert "message" in response.json()
