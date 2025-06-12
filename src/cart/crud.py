from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Cart, CartItem
from datetime import datetime

async def get_cart_by_user(session: AsyncSession, user_id: int):
    result = await session.execute(select(Cart).where(Cart.user_id == user_id))
    return result.scalar_one_or_none()

async def create_cart_for_user(session: AsyncSession, user_id: int):
    cart = Cart(user_id=user_id)
    session.add(cart)
    await session.commit()
    await session.refresh(cart)
    return cart

async def add_movie_to_cart(session: AsyncSession, cart: Cart, movie_id: int):
    # Prevent duplicate movies
    for item in cart.items:
        if item.movie_id == movie_id:
            return None
    item = CartItem(cart_id=cart.id, movie_id=movie_id, added_at=datetime.utcnow())
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item

async def remove_movie_from_cart(session: AsyncSession, cart: Cart, movie_id: int):
    item = next((i for i in cart.items if i.movie_id == movie_id), None)
    if item:
        await session.delete(item)
        await session.commit()
        return True
    return False

async def clear_cart(session: AsyncSession, cart: Cart):
    for item in list(cart.items):
        await session.delete(item)
    await session.commit()
