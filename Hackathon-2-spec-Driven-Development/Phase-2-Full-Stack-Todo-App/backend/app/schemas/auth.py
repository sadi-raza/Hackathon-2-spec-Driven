from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    """Schema for user signup request."""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="User's password (min 8 characters)")


class LoginRequest(BaseModel):
    """Schema for user login request."""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class UserResponse(BaseModel):
    """Schema for user data in responses."""
    id: str
    email: str
    name: str | None = None
    createdAt: str

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    """Schema for authentication response with token and user data."""
    token: str
    user: UserResponse


class LogoutResponse(BaseModel):
    """Schema for logout response."""
    message: str = "Logged out successfully"
