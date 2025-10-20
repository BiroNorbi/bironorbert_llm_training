"""
Migration script to add reserved_stock column to products table
and create cart_items table.

Run this script once to migrate existing database.
"""
import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

async def migrate():
    engine = create_async_engine(DATABASE_URL, echo=True)
    
    async with engine.begin() as conn:
        # Add reserved_stock column to products table
        try:
            await conn.execute(text(
                "ALTER TABLE products ADD COLUMN reserved_stock INTEGER DEFAULT 0"
            ))
            print("✓ Added reserved_stock column to products table")
        except Exception as e:
            if "duplicate column name" in str(e).lower():
                print("✓ reserved_stock column already exists")
            else:
                print(f"Error adding reserved_stock column: {e}")
        
        # Create cart_items table
        try:
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS cart_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER DEFAULT 1 NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products(id)
                )
            """))
            print("✓ Created cart_items table")
        except Exception as e:
            print(f"Error creating cart_items table: {e}")
    
    await engine.dispose()
    print("\n✓ Migration completed successfully!")

if __name__ == "__main__":
    asyncio.run(migrate())
