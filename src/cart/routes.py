from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_async_session
from .schemas import CartSchema, CartAddItemSchema, CartRemoveItemSchema
from .crud import get_cart_by_user, create_cart_for_user, add_movie_to_cart, remove_movie_from_cart, clear_cart

router = APIRouter(prefix="/cart", tags=["cart"])

def get_current_user_id():
    # TODO: Replace with actual auth
    return 1

@router.get("/", response_model=CartSchema)
async def get_cart(session: AsyncSession = Depends(get_async_session)):
    user_id = get_current_user_id()
    cart = await get_cart_by_user(session, user_id)
    if not cart:
        cart = await create_cart_for_user(session, user_id)
    return cart

@router.post("/add", response_model=CartSchema)
async def add_item(item: CartAddItemSchema, session: AsyncSession = Depends(get_async_session)):
    user_id = get_current_user_id()
    cart = await get_cart_by_user(session, user_id)
    if not cart:
        cart = await create_cart_for_user(session, user_id)
    result = await add_movie_to_cart(session, cart, item.movie_id)
    if result is None:
        raise HTTPException(status_code=400, detail="Movie already in cart")
    return await get_cart_by_user(session, user_id)

@router.post("/remove", response_model=CartSchema)
async def remove_item(item: CartRemoveItemSchema, session: AsyncSession = Depends(get_async_session)):
    user_id = get_current_user_id()
    cart = await get_cart_by_user(session, user_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    removed = await remove_movie_from_cart(session, cart, item.movie_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Movie not found in cart")
    return await get_cart_by_user(session, user_id)

@router.post("/clear", response_model=CartSchema)
async def clear(session: AsyncSession = Depends(get_async_session)):
    user_id = get_current_user_id()
    cart = await get_cart_by_user(session, user_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    await clear_cart(session, cart)
    return await get_cart_by_user(session, user_id)
