from pydantic import BaseModel


class ProductIn(BaseModel):
    title: str
    description: str
    department: str
    price: float
    quantity: int
