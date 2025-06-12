from pydantic import BaseModel, EmailStr, Field, constr
from typing import Optional
from datetime import datetime
from .enums import UserGroupEnum, GenderEnum

class UserProfileSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[GenderEnum] = None
    date_of_birth: Optional[datetime] = None
    info: Optional[str] = None

    class Config:
        orm_mode = True

class UserSchema(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime
    group: UserGroupEnum
    profile: Optional[UserProfileSchema] = None

    class Config:
        orm_mode = True

class UserCreateSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
    group: UserGroupEnum = UserGroupEnum.USER

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class PasswordChangeSchema(BaseModel):
    old_password: str
    new_password: constr(min_length=8)

class PasswordResetRequestSchema(BaseModel):
    email: EmailStr

class PasswordResetConfirmSchema(BaseModel):
    token: str
    new_password: constr(min_length=8)
