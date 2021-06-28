import pytest
from httpx import AsyncClient

from src import main


@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=main.app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"health": "ok"}

@pytest.mark.asyncio
async def test_router_hello():
    _test_name = 'tester'
    async with AsyncClient(app=main.app, base_url="http://localhost:8000") as ac:
        response_without_data = await ac.post(
            "/router/hello",
            json={}
        )
        response_with_data = await ac.post(
            "/router/hello",
            json={'name': _test_name}
        )

    assert response_without_data.status_code == 200
    assert response_without_data.json() == {"router": "says hello"}

    assert response_with_data.status_code == 200
    assert response_with_data.json() == {"router": f"welcome back {_test_name}"}
