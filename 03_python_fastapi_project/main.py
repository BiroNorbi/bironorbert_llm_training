from fastapi import Depends, FastAPI, HTTPException
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import create_tables, get_db, Product as Prod, CartItem as CartItemModel

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

class CartItemResponseDTO(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_price: float
    quantity: int
    total_price: float

class AddToCartDTO(BaseModel):
    product_id: int
    quantity: int = 1 

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

# Cart endpoints
@app.post("/cart/add", response_model=CartItemResponseDTO, status_code=201)
async def add_to_cart(cart_data: AddToCartDTO, db: AsyncSession = Depends(get_db)) -> CartItemResponseDTO:
    """Add a product to the cart"""
    try:
        # Check if product exists
        result = await db.execute(select(Prod).where(Prod.id == cart_data.product_id))
        product = result.scalars().first()
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching product: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    try:
        # Ensure reserved_stock is not None
        if product.reserved_stock is None:
            product.reserved_stock = 0
            await db.commit()
            await db.refresh(product)
        
        # Check available stock (stock - reserved_stock)
        available_stock = product.stock - product.reserved_stock
        if available_stock < cart_data.quantity:
            raise HTTPException(
                status_code=400, 
                detail=f"Not enough stock available. Available: {available_stock}"
            )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error checking stock: {e}")
        raise HTTPException(status_code=500, detail=f"Stock check error: {str(e)}")
    
    try:
        # Check if product already in cart
        cart_result = await db.execute(
            select(CartItemModel).where(CartItemModel.product_id == cart_data.product_id)
        )
        existing_cart_item = cart_result.scalars().first()
    except Exception as e:
        print(f"Error checking existing cart item: {e}")
        raise HTTPException(status_code=500, detail=f"Cart check error: {str(e)}")
    
    try:
        # Store product details BEFORE any commits to avoid lazy loading issues
        product_id = product.id
        product_name = product.name
        product_price = float(product.price)
        
        if existing_cart_item:
            # Update quantity
            new_quantity = existing_cart_item.quantity + cart_data.quantity
            quantity_difference = cart_data.quantity  # Additional items being added
            
            if available_stock < quantity_difference:
                raise HTTPException(
                    status_code=400,
                    detail=f"Not enough stock available. Available: {available_stock}"
                )
            
            # Decrement stock and update reserved stock
            product.stock -= quantity_difference
            product.reserved_stock += quantity_difference
            existing_cart_item.quantity = new_quantity
            
            # Store cart item ID before commit
            cart_item_id = existing_cart_item.id
            cart_item_quantity = new_quantity
            
            await db.commit()
            
            return CartItemResponseDTO(
                id=cart_item_id,
                product_id=product_id,
                product_name=product_name,
                product_price=product_price,
                quantity=cart_item_quantity,
                total_price=product_price * cart_item_quantity
            )
        else:
            # Create new cart item
            new_cart_item = CartItemModel(
                product_id=cart_data.product_id,
                quantity=cart_data.quantity
            )
            
            # Decrement stock and reserve it
            product.stock -= cart_data.quantity
            product.reserved_stock += cart_data.quantity
            
            db.add(new_cart_item)
            await db.commit()
            await db.refresh(new_cart_item)
            
            # Get the ID after commit
            cart_item_id = new_cart_item.id
            
            return CartItemResponseDTO(
                id=cart_item_id,
                product_id=product_id,
                product_name=product_name,
                product_price=product_price,
                quantity=cart_data.quantity,
                total_price=product_price * cart_data.quantity
            )
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        print(f"Error adding to cart: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to add to cart: {str(e)}")

@app.get("/cart", response_model=list[CartItemResponseDTO])
async def get_cart(db: AsyncSession = Depends(get_db)) -> list[CartItemResponseDTO]:
    """Get all items in the cart"""
    # Use selectinload to eagerly load the product relationship
    result = await db.execute(
        select(CartItemModel).options(selectinload(CartItemModel.product))
    )
    cart_items = result.scalars().all()
    
    response = []
    for item in cart_items:
        if item.product:
            response.append(CartItemResponseDTO(
                id=item.id,
                product_id=item.product.id,
                product_name=item.product.name,
                product_price=float(item.product.price),
                quantity=item.quantity,
                total_price=float(item.product.price) * item.quantity
            ))
    
    return response

@app.delete("/cart/{cart_item_id}", status_code=204)
async def remove_from_cart(cart_item_id: int, db: AsyncSession = Depends(get_db)):
    """Remove an item from the cart"""
    result = await db.execute(select(CartItemModel).where(CartItemModel.id == cart_item_id))
    cart_item = result.scalars().first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    # Restore stock and release reserved stock
    product_result = await db.execute(select(Prod).where(Prod.id == cart_item.product_id))
    product = product_result.scalars().first()
    
    if product:
        product.stock += cart_item.quantity  # Restore the stock
        product.reserved_stock -= cart_item.quantity  # Release reserved stock
    
    await db.delete(cart_item)
    await db.commit()

@app.delete("/cart", status_code=204)
async def clear_cart(db: AsyncSession = Depends(get_db)):
    """Clear all items from the cart"""
    result = await db.execute(select(CartItemModel))
    cart_items = result.scalars().all()
    
    # Restore stock and release all reserved stock
    for item in cart_items:
        product_result = await db.execute(select(Prod).where(Prod.id == item.product_id))
        product = product_result.scalars().first()
        if product:
            product.stock += item.quantity  # Restore the stock
            product.reserved_stock -= item.quantity  # Release reserved stock
        await db.delete(item)
    
    await db.commit()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000)
