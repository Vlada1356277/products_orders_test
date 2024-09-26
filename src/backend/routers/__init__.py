from fastapi import APIRouter
from .orders import router as orders_router
from .products import router as products_router

router = APIRouter()

router.include_router(
    orders_router
)

router.include_router(
    products_router
)
