from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db, Product
from schemas.products import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix='/products')

@router.post("", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    product_exist = await db.execute(
        select(Product).filter(Product.name == product.name)
    )
    product_exist = product_exist.scalars().first()

    if product_exist:
        raise HTTPException(status_code=400, detail="Продукт с этим именем уже создан")

    new_product = Product(name=product.name,
                          description=product.description,
                          price=product.price,
                          stock_quantity=product.stock_quantity)

    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)

    return new_product


@router.get("", response_model=list[ProductResponse])
async def get_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    products = result.scalars().all()
    return products


@router.get("/{id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).filter(Product.id == product_id))
    product = result.scalars().first()

    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    return product


@router.put("/{id}", response_model=ProductResponse)
async def update_product(product_id: int, product_data: ProductUpdate, db: AsyncSession = Depends(get_db)):
    product = await db.get(Product, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")

    update_data = product_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(product, key, value)

    await db.commit()
    await db.refresh(product)
    return product


@router.delete("/{id}", status_code=204)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await db.get(Product, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Продукт не найден")

    await db.delete(product)
    await db.commit()
    return None