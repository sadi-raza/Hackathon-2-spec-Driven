from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from datetime import datetime, timedelta, timezone
import jwt
import uuid

from ..models.user import User
from ..config import settings


class AuthService:
    """Service for authentication operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_user(self, email: str, password: str) -> User:
        """Create a new user with hashed password."""
        # Check if user already exists
        existing = await self.get_user_by_email(email)
        if existing:
            raise ValueError("User with this email already exists")
        
        user = User(
            id=str(uuid.uuid4()),
            email=email,
            hashed_password=User.hash_password(password),
        )
        
        self.db.add(user)
        await self.db.flush()
        return user
    
    async def get_user_by_email(self, email: str) -> User | None:
        """Get a user by email address."""
        statement = select(User).where(User.email == email)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()
    
    async def get_user_by_id(self, user_id: str) -> User | None:
        """Get a user by ID."""
        statement = select(User).where(User.id == user_id)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()
    
    async def authenticate_user(self, email: str, password: str) -> User | None:
        """Authenticate a user by email and password."""
        user = await self.get_user_by_email(email)
        if not user:
            return None
        if not user.verify_password(password):
            return None
        return user
    
    @staticmethod
    def create_access_token(user_id: str, expires_delta: timedelta | None = None) -> str:
        """Create a JWT access token for a user."""
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(days=7)  # Default 7 days
        
        payload = {
            "sub": user_id,
            "userId": user_id,  # For compatibility with frontend
            "exp": expire,
            "iat": datetime.now(timezone.utc),
        }
        
        return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
