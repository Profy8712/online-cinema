from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional

class CartItemSchema(BaseModel):
    id: int
    movie_id: int
    added_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CartSchema(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    items: List[CartItemSchema] = []

    model_config = ConfigDict(from_attributes=True)

class CartAddItemSchema(BaseModel):
    movie_id: int

class CartRemoveItemSchema(BaseModel):
    movie_id: int
