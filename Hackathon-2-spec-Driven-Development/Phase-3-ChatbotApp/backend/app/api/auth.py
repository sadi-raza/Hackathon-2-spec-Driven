from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.auth import (
    SignupRequest, LoginRequest, AuthResponse, 
    UserResponse, LogoutResponse
)
from ..services.auth_service import AuthService
from ..database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=AuthResponse, status_code=201)
async def signup(
    request: SignupRequest,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user account."""
    auth_service = AuthService(db)
    
    try:
        user = await auth_service.create_user(
            email=request.email,
            password=request.password
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    
    token = AuthService.create_access_token(user.id)
    
    return AuthResponse(
        token=token,
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            createdAt=user.created_at.isoformat()
        )
    )


@router.post("/login", response_model=AuthResponse)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """Login with email and password."""
    auth_service = AuthService(db)
    
    user = await auth_service.authenticate_user(
        email=request.email,
        password=request.password
    )
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = AuthService.create_access_token(user.id)
    
    return AuthResponse(
        token=token,
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            createdAt=user.created_at.isoformat()
        )
    )


@router.post("/logout", response_model=LogoutResponse)
async def logout():
    """Logout the current user (token invalidation handled client-side)."""
    # For JWT-based auth, logout is handled client-side by removing the token
    # A more robust solution would use a token blacklist
    return LogoutResponse()
