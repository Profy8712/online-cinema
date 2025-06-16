from pydantic import BaseModel, EmailStr, constr, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)

class UserSchema(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime
    group: UserGroupEnum
    profile: Optional[UserProfileSchema] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj):
        # If your model property is not named exactly as in schema, map it
        return cls(
            id=obj.id,
            email=obj.email,
            is_active=obj.is_active,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
            group=getattr(obj.group, "name", None),
            profile=obj.profile
        )

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
