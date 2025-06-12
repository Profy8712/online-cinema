from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from .models import Order, OrderItem, OrderStatusEnum
from src.movies.models import Movie
from decimal import Decimal

async def get_orders_by_user(session: AsyncSession, user_id: int):
    result = await session.execute(select(Order).where(Order.user_id == user_id))
    return result.scalars().all()

async def get_order_by_id(session: AsyncSession, order_id: int):
    result = await session.execute(select(Order).where(Order.id == order_id))
    return result.scalar_one_or_none()

async def create_order(session: AsyncSession, user_id: int, movie_ids: list[int]):
    # Проверка фильмов
    movies = (await session.execute(select(Movie).where(Movie.id.in_(movie_ids)))).scalars().all()
    if not movies:
        return None
    total = sum(Decimal(str(m.price)) for m in movies)
    order = Order(user_id=user_id, status=OrderStatusEnum.pending, total_amount=total)
    session.add(order)
    await session.flush()  # get order.id

    for m in movies:
        session.add(OrderItem(order_id=order.id, movie_id=m.id, price_at_order=m.price))
    await session.commit()
    await session.refresh(order)
    return order
