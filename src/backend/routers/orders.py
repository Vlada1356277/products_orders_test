from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import defer, selectinload
from database import Order, get_db, Product, OrderItem
from schemas.orders import OrderResponse, OrderCreate, OrderStatusUpdate

router = APIRouter(
    prefix='/orders',
    tags=['Orders'])

@router.post('', status_code=status.HTTP_201_CREATED, response_model=OrderResponse)
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):

    new_order = Order(status="в процессе")
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)

    for item in order.order_items:
        product = await db.get(Product, item.product_id)
        if not product or product.stock_quantity < item.quantity:
            raise HTTPException(status_code=400,
                                detail=f"Товара {product.name} недостаточно на складе. Доступно: {product.stock_quantity}")

        order_item = OrderItem(order_id=new_order.id, product_id=item.product_id, quantity=item.quantity)
        product.stock_quantity -= item.quantity
        db.add(order_item)

    await db.commit()

    query = select(Order).options(selectinload(Order.order_items)).filter(Order.id == new_order.id)
    result = await db.execute(query)
    new_order = result.scalars().first()

    return new_order


@router.get("", response_model=List[OrderResponse])
async def get_orders(db: AsyncSession = Depends(get_db)):
    orders = await db.execute(select(Order).options(selectinload(Order.order_items)))
    return orders.scalars().all()


@router.get("/{id}", response_model=OrderResponse)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await db.get(Order, order_id, options=[selectinload(Order.order_items)])
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order


@router.patch("/{id}/status", response_model=OrderResponse)
async def update_order_status(order_id: int, status_data: OrderStatusUpdate, db: AsyncSession = Depends(get_db)):
    query = select(Order).options(selectinload(Order.order_items)).filter(Order.id == order_id)
    result = await db.execute(query)
    order = result.scalars().first()

    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    order.status = status_data.status
    await db.commit()
    await db.refresh(order)
    return order