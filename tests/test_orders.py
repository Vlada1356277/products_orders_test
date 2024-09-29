import pytest
from httpx import ASGITransport, AsyncClient

from src.backend.main import app

@pytest.mark.asyncio
async def test_create_order():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:

        order_data = {
            "order_items": [
                {"product_id": 7, "quantity": 1},
                {"product_id": 8, "quantity": 1}
            ]
        }

        response = await ac.post("/orders", json=order_data)

        print(response.json())
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "в процессе"