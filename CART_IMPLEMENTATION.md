# Shopping Cart Feature Implementation

## Summary
This implementation adds a shopping cart feature to both the backend (FastAPI) and frontend (Angular) applications.

## Backend Changes (03_python_fastapi_project)

### 1. Database Changes (`database.py`)
- Added `reserved_stock` column to `Product` model to track stock reserved in carts
- Added new `CartItem` model with fields:
  - `id`: Primary key
  - `product_id`: Foreign key to products
  - `quantity`: Number of items in cart
  - `created_at`: Timestamp

### 2. API Endpoints (`main.py`)
Added new DTOs:
- `CartItemResponseDTO`: Response format for cart items
- `AddToCartDTO`: Request format for adding items to cart

Added new endpoints:
- `POST /cart/add`: Add a product to cart
  - Validates product exists
  - Checks available stock (stock - reserved_stock)
  - Updates existing cart item or creates new one
  - Reserves stock automatically
  
- `GET /cart`: Get all cart items
  - Returns list of cart items with product details
  
- `DELETE /cart/{cart_item_id}`: Remove item from cart
  - Releases reserved stock
  
- `DELETE /cart`: Clear entire cart
  - Releases all reserved stock

## Frontend Changes (05_design/product-management-app)

### 1. Models (`src/app/models/product.model.ts`)
Added interfaces:
- `CartItem`: Cart item structure
- `AddToCart`: Request structure for adding to cart

### 2. Cart Service (`src/app/services/cart.service.ts`)
New service with:
- `cartItems` and `cartItemsCount` signals for reactive state
- `getCart()`: Fetch cart items
- `addToCart()`: Add product to cart
- `removeFromCart()`: Remove item from cart
- `clearCart()`: Clear all cart items

### 3. Cart Component (`src/app/components/cart/`)
New component displayed in bottom-left corner:
- Expandable/collapsible cart widget
- Shows cart item count badge
- Lists all cart items with quantity and price
- Remove item buttons
- Total price calculation
- Clear cart button
- Styled with modern, clean UI

### 4. Product List Updates (`src/app/components/product-list/`)
- Added green "+" button next to each product
- Clicking "+" adds product to cart
- Shows error if insufficient stock
- Refreshes product list after adding to cart

### 5. App Component (`src/app/app.ts` & `app.html`)
- Integrated CartComponent globally so it appears on all pages

## Features

✅ **Stock Management**
- Available stock = total stock - reserved stock
- Stock is automatically reserved when added to cart
- Stock is released when removed from cart
- Prevents overselling

✅ **User Experience**
- Visual "+" button on each product
- Cart widget in bottom-left corner
- Expandable cart view
- Item count badge
- Total price display
- Error handling for out-of-stock items

✅ **API Integration**
- Full CRUD operations for cart
- Proper error handling
- Stock validation

## How to Use

1. **Backend**: Start the FastAPI server (the database will auto-create new tables)
2. **Frontend**: The cart icon will appear in the bottom-left corner
3. **Add to Cart**: Click the green "+" button on any product
4. **View Cart**: Click the cart widget to expand/collapse
5. **Remove Items**: Click the "X" button next to any cart item
6. **Clear Cart**: Click "Clear Cart" button to remove all items

## Database Migration Note
The database will automatically create the new `cart_items` table and add the `reserved_stock` column to the `products` table when you restart the backend server.
