from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime
from typing import Optional
from enum import Enum


class UserRole(str, Enum):
    """User roles enum"""
    MANAGER = "manager"
    DOCTOR = "shifokor"
    NURSE = "amaliyot_hamshirasi"
    RECEPTIONIST = "royhatga_oluvchi"
    PATRONAGE_NURSE = "patronaj_hamshirasi"


class UserBase(BaseModel):
    full_name: str
    jshshir: str = Field(..., min_length=14, max_length=14, description="14-digit passport number")
    roles: list[UserRole]
    gender: str
    birth_date: date
    phone: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new user (password will be auto-generated)"""
    pass


class UserUpdate(BaseModel):
    """Schema for updating user"""
    full_name: Optional[str] = None
    jshshir: Optional[str] = Field(None, min_length=14, max_length=14)
    roles: Optional[list[UserRole]] = None
    gender: Optional[str] = None
    birth_date: Optional[date] = None
    phone: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response (includes password for admin)"""
    id: int
    password: str  # Plain text password visible to admin
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserListResponse(BaseModel):
    """Schema for user list response"""
    id: int
    full_name: str
    jshshir: str
    password: str
    roles: list[str]
    phone: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
