from fastapi import Depends, FastAPI, HTTPException
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import create_tables, get_db, Product as Prod

class Product(BaseModel):
    id: int
    name: str 
    price: float 
    description : str | None = None
    stock: int 

class ProductCreateDTO(BaseModel):
    name: str 
    price: float
    description: str | None = None
    stock: int | None = None

class ProductUpdateDTO(BaseModel):
    name: str | None = None
    price: float | None = None
    description : str | None = None
    stock: int | None = None

class ProductResponseDTO(BaseModel):
    id: int
    name: str 
    price: float 
    description : str | None = None
    stock: int 

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(
    title="FastAPI Product API",
    description="A simple FastAPI application for managing products",
    version="0.1.0",
    lifespan=lifespan
)

# CORS is handled by Nginx - no need for FastAPI middleware when using reverse proxy
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Product API"}

@app.get("/products", response_model=list[ProductResponseDTO])
async def get_all_products(db: AsyncSession = Depends(get_db)) -> list[ProductResponseDTO]:
    """Get all products from the database"""
    result = await db.execute(select(Prod))
    products = result.scalars().all()
    
    return [
        ProductResponseDTO(
            id=product.id,
            name=product.name,
            price=float(product.price),
            description=product.description,
            stock=product.stock
        )
        for product in products
    ]

@app.post("/products", response_model=ProductResponseDTO, status_code=201)
async def create_product(product: ProductCreateDTO, db: AsyncSession = Depends(get_db)) -> ProductResponseDTO:
    """Create a new product in the database"""

    new_product = Prod(
        name=product.name,
        price=product.price,
        description=product.description,
        stock=product.stock if product.stock is not None else 0
    )
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    
    return ProductResponseDTO(
        id=new_product.id,
        name=new_product.name,
        price=float(new_product.price),
        description=new_product.description,
        stock=new_product.stock
    )

@app.put("/products/{product_id}", response_model=ProductResponseDTO)
async def update_product(product_id: int, product: ProductUpdateDTO, db: AsyncSession = Depends(get_db)) -> ProductResponseDTO:
    """Update an existing product in the database"""
    result = await db.execute(select(Prod).where(Prod.id == product_id))
    existing_product = result.scalars().first()
    
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.name is not None:
        existing_product.name = product.name
    if product.price is not None:
        existing_product.price = product.price
    if product.description is not None:
        existing_product.description = product.description
    if product.stock is not None:
        existing_product.stock = product.stock

    db.add(existing_product)
    await db.commit()
    await db.refresh(existing_product)
    
    return ProductResponseDTO(
        id=existing_product.id,
        name=existing_product.name,
        price=float(existing_product.price),
        description=existing_product.description,
        stock=existing_product.stock
    )

@app.get("/products/{product_id}", response_model=ProductResponseDTO)
async def get_product_by_id(product_id: int, db: AsyncSession = Depends(get_db)) -> ProductResponseDTO:
    result = await db.execute(select(Prod).where(Prod.id == product_id))
    product = result.scalars().first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found by ID")
    
    return ProductResponseDTO(
        id=product.id,
        name=product.name,
        price=float(product.price),
        description=product.description,
        stock=product.stock
    )

@app.delete("/products/{product_id}", status_code=204)
async def delete_product_by_id(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Prod).where(Prod.id == product_id))
    product = result.scalars().first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found by ID")
    
    await db.delete(product)
    await db.commit()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000)
