from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    description: str = None
    price: float
    stock_quantity: int

class ProductResponse(BaseModel):
    id: int
    price: float
    name: str
    description: str
    stock_quantity: int


class ProductUpdate(BaseModel):
    name: str = None
    description: str = None
    price: float = None
    stock_quantity: int = None


