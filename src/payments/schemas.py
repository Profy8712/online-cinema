from pydantic import BaseModel, condecimal
from typing import List, Optional
from decimal import Decimal
from datetime import datetime

class PaymentItemSchema(BaseModel):
    id: int
    order_item_id: int
    price_at_payment: condecimal(max_digits=10, decimal_places=2)

    class Config:
        from_attributes = True  # вместо устаревшего orm_mode

class PaymentSchema(BaseModel):
    id: int
    user_id: int
    order_id: int
    created_at: datetime
    status: str
    amount: Decimal
    external_payment_id: Optional[str] = None
    items: List[PaymentItemSchema]

    class Config:
        from_attributes = True

class PaymentCreateSchema(BaseModel):
    order_id: int
    amount: condecimal(max_digits=10, decimal_places=2)
