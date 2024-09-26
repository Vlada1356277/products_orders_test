from itertools import product

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from setuptools.extern import names
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from database import get_db, Product
from schemas.products import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix='/products')

@router.post("", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    product_exist = db.query(Product).filter(Product.name == product.name).first()
    if product_exist:
        raise HTTPException(status_code=400, detail="Продукт с этим именем уже создан")

    new_product = Product(name=product.name,
                          description=product.description,
                          price=product.price,
                          stock_quantity=product.stock_quantity)

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@router.get("", response_model=list[ProductResponse])
async def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products


@router.get("", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    return product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product_data: ProductUpdate, db: AsyncSession = Depends(get_db)):
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")

    update_data = jsonable_encoder(product_data)

    for key, value in update_data.items():
        setattr(product, key, value)

    await db.commit()
    await db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")

    db.delete(product)
    db.commit()
    return None