from sqlalchemy import (
    Column, Integer, ForeignKey, DateTime, Enum, DECIMAL, String
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class PaymentStatusEnum(str, enum.Enum):
    successful = "successful"
    canceled = "canceled"
    refunded = "refunded"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(PaymentStatusEnum), nullable=False, default=PaymentStatusEnum.successful)
    amount = Column(DECIMAL(10, 2), nullable=False)
    external_payment_id = Column(String, nullable=True)

    user = relationship("User", backref="payments")
    order = relationship("Order", backref="payments")
    items = relationship("PaymentItem", back_populates="payment")

class PaymentItem(Base):
    __tablename__ = "payment_items"

    id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=False)
    order_item_id = Column(Integer, ForeignKey("order_items.id"), nullable=False)
    price_at_payment = Column(DECIMAL(10, 2), nullable=False)

    payment = relationship("Payment", back_populates="items")
    # Optionally, relationship to OrderItem
