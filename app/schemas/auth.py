from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Schema for login request"""
    jshshir: str = Field(..., min_length=14, max_length=14, description="14-digit passport number")
    password: str = Field(..., min_length=6, max_length=6, description="6-digit password")


class LoginResponse(BaseModel):
    """Schema for login response"""
    access_token: str
    token_type: str = "bearer"
    user: dict  # User information
