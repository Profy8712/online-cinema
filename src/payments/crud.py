from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Payment, PaymentItem, PaymentStatusEnum
from src.orders.models import Order, OrderItem

async def create_payment(session: AsyncSession, user_id: int, order_id: int, amount: float, external_payment_id: str):
    payment = Payment(
        user_id=user_id,
        order_id=order_id,
        amount=amount,
        status=PaymentStatusEnum.successful,
        external_payment_id=external_payment_id
    )
    session.add(payment)
    await session.flush()  # get payment.id

    # Add all order_items to payment_items
    order_items = (await session.execute(
        select(OrderItem).where(OrderItem.order_id == order_id)
    )).scalars().all()
    for item in order_items:
        session.add(PaymentItem(
            payment_id=payment.id,
            order_item_id=item.id,
            price_at_payment=item.price_at_order
        ))
    await session.commit()
    await session.refresh(payment)
    return payment
