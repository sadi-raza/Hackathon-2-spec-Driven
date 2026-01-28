from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
import bcrypt

if TYPE_CHECKING:
    from .task import Task
    from .conversation import Conversation


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)
    name: str | None = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="owner")

    # Relationship to conversations (Phase III)
    conversations: List["Conversation"] = Relationship(back_populates="owner")

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password: str) -> bool:
        """Verify a password against the stored hash."""
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))
