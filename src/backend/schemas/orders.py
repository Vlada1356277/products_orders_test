from pydantic import BaseModel
from typing import Literal, List
from datetime import datetime

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    order_items: List[OrderItemCreate]


class OrderResponse(BaseModel):
    id: int
    created_at: datetime
    status: str
    order_items: List[OrderItemCreate]

    model_config = {
        'from_attributes': True
    }


class OrderStatusUpdate(BaseModel):
    status: Literal["в процессе", "отправлен", "доставлен"]
