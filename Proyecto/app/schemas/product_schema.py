# app/schemas/product_schema.py
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    brand: str
    price: float
    stock: int
    payment_method: str  # nuevo campo agregado

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True
