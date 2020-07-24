from typing import List

from pydantic import BaseModel


class ProductIn(BaseModel):
    product_id: str
    amount: int


class ProductOut(BaseModel):
    id: str
    amount: int
    price: float


class CartOut(BaseModel):
    id: str
    total_price: float
    products: List[ProductOut]
