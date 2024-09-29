import pytest
from httpx import ASGITransport, AsyncClient

from src.backend.main import app


@pytest.mark.asyncio
async def test_create_product():
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:

        product_data = {
            "name": "Тестовый продукт12",
            "description": "Описание тестового продукта",
            "price": 100.0,
            "stock_quantity": 50
        }

        response = await ac.post("/products", json=product_data)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == product_data["name"]
        assert data["price"] == product_data["price"]
        assert data["stock_quantity"] == product_data["stock_quantity"]