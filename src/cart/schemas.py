from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class CartItemSchema(BaseModel):
    id: int
    movie_id: int
    added_at: datetime

    class Config:
        orm_mode = True

class CartSchema(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    items: List[CartItemSchema] = []

    class Config:
        orm_mode = True

class CartAddItemSchema(BaseModel):
    movie_id: int

class CartRemoveItemSchema(BaseModel):
    movie_id: int
