from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_async_session
from .schemas import UserCreateSchema, UserLoginSchema, UserSchema, TokenSchema
from .models import User, UserGroup, ActivationToken
from .password_utils import hash_password, verify_password
from .jwt_utils import create_access_token, create_refresh_token
from sqlalchemy.future import select
import uuid
from datetime import datetime, timedelta

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.post("/register", response_model=UserSchema)
async def register(user: UserCreateSchema, session: AsyncSession = Depends(get_async_session)):
    # Check if user with this email already exists
    result = await session.execute(select(User).where(User.email == user.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email already registered")

    # Check if the group exists
    group_result = await session.execute(select(UserGroup).where(UserGroup.name == user.group))
    group = group_result.scalar_one_or_none()
    if not group:
        raise HTTPException(status_code=400, detail="User group does not exist")

    db_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        group_id=group.id,
        is_active=False
    )
    session.add(db_user)
    await session.flush()
    token_str = str(uuid.uuid4())
    activation_token = ActivationToken(
        user_id=db_user.id,
        token=token_str,
        expires_at=datetime.utcnow() + timedelta(hours=24)
    )
    session.add(activation_token)
    await session.commit()
    await session.refresh(db_user)
    # TODO: send activation email with token
    return db_user

@router.post("/login", response_model=TokenSchema)
async def login(data: UserLoginSchema, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is not activated")
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.get("/activate")
async def activate(token: str, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(ActivationToken).where(ActivationToken.token == token))
    activation_token = result.scalar_one_or_none()
    if not activation_token or activation_token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user = await session.get(User, activation_token.user_id)
    user.is_active = True
    session.delete(activation_token)
    await session.commit()
    return {"detail": "Account activated successfully"}
