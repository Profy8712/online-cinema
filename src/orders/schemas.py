from pydantic import BaseModel, condecimal, ConfigDict
from typing import List
from decimal import Decimal
from datetime import datetime

class OrderItemSchema(BaseModel):
    id: int
    movie_id: int
    price_at_order: condecimal(max_digits=10, decimal_places=2)

    model_config = ConfigDict(from_attributes=True)

class OrderSchema(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    status: str
    total_amount: Decimal
    items: List[OrderItemSchema]

    model_config = ConfigDict(from_attributes=True)

class OrderCreateSchema(BaseModel):
    movie_ids: List[int]
