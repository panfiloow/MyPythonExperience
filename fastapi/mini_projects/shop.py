from decimal import Decimal
from enum import Enum
import re
from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, field_validator
import uvicorn

app = FastAPI()

class Category(str, Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    BOOKS = "books"
    HOME = "home"
    SPORTS = "sports"

class Product(BaseModel):
    id: int
    sku: str  # Артикул
    name: str
    description: Optional[str] = None
    price: Decimal
    category: Category
    stock_quantity: int
    is_active: bool = True
    tags: List[str] = []
    
    @field_validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v
    
    @field_validator('stock_quantity')
    def validate_stock(cls, v):
        if v < 0:
            raise ValueError('Stock quantity cannot be negative')
        return v
    
    @field_validator('sku')
    def validate_sku(cls, v):
        if len(v) < 3:
            raise ValueError('SKU must be at least 3 characters long')
        return v.upper()


class User(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str] = None
    is_active: bool = True
    is_vip: bool = False
    
    @field_validator('phone')
    def validate_phone(cls, v):
        if v and not re.match(r'^\+?[1-9]\d{1,14}$', v):
            raise ValueError('Invalid phone number format')
        return v
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class CartItem(BaseModel):
    product_id: int
    quantity: int
    unit_price: Decimal
    
    @field_validator('quantity')
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v

class ShoppingCart(BaseModel):
    user_id: int
    items: List[CartItem] = []
    
    @property
    def total_amount(self) -> Decimal:
        return sum(item.unit_price * item.quantity for item in self.items)
    
    @property
    def total_items(self) -> int:
        return sum(item.quantity for item in self.items)
    
    def add_item(self, product: Product, quantity: int = 1) -> bool:
        if product.stock_quantity < quantity:
            print(f"Недостаточно товара '{product.name}'. Доступно: {product.stock_quantity}, запрошено: {quantity}")
            return False
        
        for item in self.items:
            if item.product_id == product.id:
                new_quantity = item.quantity + quantity
                
                if product.stock_quantity < new_quantity:
                    print(f"Недостаточно товара для добавления. Уже в корзине: {item.quantity}, хотим добавить: {quantity}")
                    return False
                
                item.quantity = new_quantity
                print(f"Обновлено количество товара '{product.name}': {item.quantity}")
                return True
        
        new_item = CartItem(
            product_id=product.id,
            quantity=quantity,
            unit_price=product.price
        )
        self.items.append(new_item)
        print(f"Добавлен товар '{product.name}' в количестве {quantity}")
        return True
    

@app.get("/", summary="Приветствие")
async def greatings():
    return {"message": "Добро пожаловать в наш магазин"}


if __name__ == "__main__":
    uvicorn.run("shop:app", host="127.0.0.1", port=8000, reload=True)

