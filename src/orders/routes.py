from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_async_session
from .schemas import OrderSchema, OrderCreateSchema
from .crud import get_orders_by_user, get_order_by_id, create_order

router = APIRouter(prefix="/orders", tags=["orders"])

def get_current_user_id():
    # TODO: Replace with real auth
    return 1

@router.get("/", response_model=list[OrderSchema])
async def list_orders(session: AsyncSession = Depends(get_async_session)):
    user_id = get_current_user_id()
    return await get_orders_by_user(session, user_id)

@router.get("/{order_id}", response_model=OrderSchema)
async def get_order(order_id: int, session: AsyncSession = Depends(get_async_session)):
    order = await get_order_by_id(session, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/", response_model=OrderSchema)
async def place_order(data: OrderCreateSchema, session: AsyncSession = Depends(get_async_session)):
    user_id = get_current_user_id()
    order = await create_order(session, user_id, data.movie_ids)
    if not order:
        raise HTTPException(status_code=400, detail="Cannot create order (no valid movies)")
    return order
