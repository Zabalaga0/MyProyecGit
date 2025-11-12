from pydantic import BaseModel
from datetime import date

class ProductBase(BaseModel):
    name: str
    brand: str
    price: float
    stock: int
    payment_method: str
    expiration_date: date | None = None  #Campo opcional

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True
