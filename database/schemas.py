from pydantic import BaseModel
from typing import Optional

class CartInputSchema(BaseModel):
    owner: int
class CartOutSchema(BaseModel):
    id: int
    owner: int

class CartItemInputSchema(BaseModel):
    cart: int
    product: str
    quantity: Optional[int] = None
class CartItemOutSchema(BaseModel):
    id: int
    cart: int
    product: str
    quantity: Optional[int] = None