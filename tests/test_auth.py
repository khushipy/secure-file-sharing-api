import pytest
from httpx import AsyncClient
from app.main import app
import random

@pytest.mark.asyncio
async def test_signup():
    unique_email = f"client{random.randint(1000, 9999)}@example.com"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/signup", json={
            "email": unique_email,
            "password": "testpass123",
            "role": "client"
        })
        assert response.status_code == 200
        assert "message" in response.json()

@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/login", json={
            "email": "ironman@example.com",
            "password": "ironman123"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()

