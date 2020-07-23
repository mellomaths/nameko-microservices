from pydantic import BaseModel


class ProductIn(BaseModel):
    product_id: str
    amount: int
