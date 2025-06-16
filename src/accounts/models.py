from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, DateTime, Enum as SAEnum, Text
)
from sqlalchemy.orm import relationship
from datetime import datetime
from src.db.base import Base
from .enums import UserGroupEnum, GenderEnum

class UserGroup(Base):
    __tablename__ = "user_groups"
    id = Column(Integer, primary_key=True)
    name = Column(SAEnum(UserGroupEnum), unique=True, nullable=False)
    users = relationship("User", back_populates="group")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    group_id = Column(Integer, ForeignKey("user_groups.id"), nullable=False)

    group = relationship("UserGroup", back_populates="users", lazy="joined")
    profile = relationship("UserProfile", back_populates="user", uselist=False, lazy="joined")
    activation_token = relationship("ActivationToken", back_populates="user", uselist=False)
    password_reset_token = relationship("PasswordResetToken", back_populates="user", uselist=False)
    refresh_tokens = relationship("RefreshToken", back_populates="user")

    @property
    def group_enum(self):
        return self.group.name if self.group else None

class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    avatar = Column(String)
    gender = Column(SAEnum(GenderEnum))
    date_of_birth = Column(DateTime)
    info = Column(Text)

    user = relationship("User", back_populates="profile")

class ActivationToken(Base):
    __tablename__ = "activation_tokens"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    token = Column(String, unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="activation_token")

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    token = Column(String, unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="password_reset_token")

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="refresh_tokens")
