from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from contextlib import asynccontextmanager
from fastapi import FastAPI

# Import settings first to ensure .env is loaded
from .config import settings

# Import all models to register them with SQLModel metadata
# This ensures create_all() knows about all tables
from .models import User, Task, Conversation, Message  # noqa: F401


# Database URL from settings (loaded from .env via pydantic-settings)
DATABASE_URL = settings.DATABASE_URL


# Create async engine - different settings for SQLite vs PostgreSQL
if DATABASE_URL.startswith("sqlite"):
    # SQLite doesn't support connection pooling options
    engine = create_async_engine(
        DATABASE_URL,
        echo=settings.DEBUG,
        connect_args={"check_same_thread": False},
    )
else:
    # PostgreSQL/Neon-optimized settings
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
        pool_size=3,           # Small for serverless
        max_overflow=2,
        pool_timeout=10,
        pool_recycle=3600,     # Recycle every hour
    )


# Create async session maker
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:
    """
    Dependency to get database session.
    Handles transaction commits and rollbacks automatically.
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI app.
    Creates tables on startup and disposes engine on shutdown.
    """
    # Startup: Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield

    # Shutdown: Dispose engine
    await engine.dispose()