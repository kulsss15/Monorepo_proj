import pytest
import httpx

@pytest.mark.asyncio
async def test_ai_service():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/health")
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_weather_service():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8001/health")
        assert response.status_code == 200
